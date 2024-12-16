import cv2
import numpy as np
import pymongo
import time
import json
from ultralytics import YOLO
import supervision as sv
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv(override=True)

# Store the last modification time of the .env file and zones file
last_modified_time = os.path.getmtime('.env')
last_zones_modified_time = os.path.getmtime(os.getenv("ZONES_FILE"))

# Load environment variables
rtsp_link = os.getenv("RTSP_LINK")
mongo_uri = os.getenv("MONGO_URI")
zones_file = os.getenv("ZONES_FILE")
mydb_name = os.getenv("MYDB")
mycol_name = os.getenv("MYCOL")

# Global variables for draggable points
dragging = False
current_point = None

# Global variables for cumulative zone counts
zone_cumulative_counts = {}

def reload_env_file_if_modified():
    global last_modified_time

    # Check if the file modification time has changed
    current_modified_time = os.path.getmtime('.env')
    if current_modified_time != last_modified_time:
        # Reload the .env file
        load_dotenv(override=True)

        # Update the global variables with the new values
        global rtsp_link, mongo_uri, zones_file, mydb_name, mycol_name
        rtsp_link = os.getenv("RTSP_LINK")
        mongo_uri = os.getenv("MONGO_URI")
        zones_file = os.getenv("ZONES_FILE")
        mydb_name = os.getenv("MYDB")
        mycol_name = os.getenv("MYCOL")

        # Update the modification time
        last_modified_time = current_modified_time

def reload_zones_file_if_modified():
    global last_zones_modified_time, zone_coords

    # Check if the zones file modification time has changed
    current_zones_modified_time = os.path.getmtime(zones_file)
    if current_zones_modified_time != last_zones_modified_time:
        # Reload the zones file
        zone_coords = load_zones()

        # Update the modification time
        last_zones_modified_time = current_zones_modified_time
        print("Zones file reloaded.")

def load_zones():
    with open(zones_file, 'r') as f:
        zones = json.load(f)
    # Dynamically load zones
    return {zone_name: np.array(zone, np.int32) for zone_name, zone in zones['zones'].items()}

def save_zones():
    zones = {zone_name: zone.tolist() for zone_name, zone in zone_coords.items()}
    with open(zones_file, 'w') as f:
        json.dump({"zones": zones}, f, indent=4)

# Load initial zone coordinates
zone_coords = load_zones()

# Initialize the global zone cumulative counts
for zone_name in zone_coords.keys():
    zone_cumulative_counts[zone_name] = 0

def init_mongodb():
    return pymongo.MongoClient(mongo_uri)

def log_to_db(client, customer_id, zone_name, dwell_time=0):
    try:
        mydb = client[mydb_name]  # Use the db name from .env
        mycol = mydb[mycol_name]  # Use the collection name from .env

        record = {
            "customer_id": int(customer_id),  # Convert to native int
            "booth_name": zone_name,
            "dwell_time": float(dwell_time),  # Ensure dwell time is a float
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Add timestamp
        }
        
        # Include the cumulative counts for each zone dynamically
        for zone_name, count in zone_cumulative_counts.items():
            record[f"{zone_name}_Count"] = int(count)  # Convert to native int

        mycol.insert_one(record)
        print(f"Logged to DB: {record}")
        
    except pymongo.errors.PyMongoError as e:
        print(f"Error logging to DB: {e}")

def get_latest_counts(client):
    try:
        mydb = client[mydb_name]  # Use the db name from .env
        mycol = mydb[mycol_name]  # Use the collection name from .env

        # Get the latest zone counts from the DB
        latest_zone_counts = {zone_name: 0 for zone_name in zone_coords.keys()}

        # Query for the latest zone counts
        latest_record = mycol.find_one({}, sort=[("_id", pymongo.DESCENDING)])

        if latest_record:
            # Extract zone counts
            for zone_name in latest_zone_counts.keys():
                if f"{zone_name}_Count" in latest_record:
                    latest_zone_counts[zone_name] = latest_record[f"{zone_name}_Count"]

        return latest_zone_counts

    except pymongo.errors.PyMongoError as e:
        print(f"Error fetching latest counts from DB: {e}")
        return {}

# Initialize the global visited_zones dictionary
visited_zones = {}

# Function to start video recording
def start_new_video_recording(cap, frame_width, frame_height):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_filename = f"/app/output/output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    video_writer = cv2.VideoWriter(video_filename, fourcc, 25, (frame_width, frame_height))
    return video_writer, video_filename

def process_frame(frame, detections, box_annotator, model, label_annotator):
    reload_zones_file_if_modified()  # Check for changes in zones file

    positions = {}
    polygon_zones = {zone_name: sv.PolygonZone(polygon=coords, triggering_anchors=[sv.Position.CENTER]) 
                     for zone_name, coords in zone_coords.items()}
    polygon_annotators = {zone_name: sv.PolygonZoneAnnotator(zone=polygon_zone, color=color)
                          for zone_name, (polygon_zone, color) in zip(polygon_zones.keys(), zip(polygon_zones.values(), [sv.Color.GREEN, sv.Color.RED, sv.Color.BLUE]))}

    for i, (xyxy, mask, confidence, class_id, tracker_id, data) in enumerate(detections):
        position = "None"
        for zone_name, polygon_zone in polygon_zones.items():
            if polygon_zone.trigger(detections=detections)[i]:
                position = zone_name  # Dynamically use zone name
                
                # Check if this tracker_id has visited the zone before
                if tracker_id not in visited_zones:
                    visited_zones[tracker_id] = set()  # Initialize visited zones for this tracker_id
                
                if zone_name not in visited_zones[tracker_id]:
                    # First time entering this zone
                    zone_cumulative_counts[zone_name] += 1
                    visited_zones[tracker_id].add(zone_name)  # Mark the zone as visited
                    print(f"Zone {zone_name} count: {zone_cumulative_counts[zone_name]}")
                
                # Update the current position for this tracker_id
                current_positions[tracker_id] = zone_name
                break
        
        positions[tracker_id] = position

    frame = box_annotator.annotate(scene=frame, detections=detections)
    frame = label_annotator.annotate(scene=frame, detections=detections)
    
    for zone_name, annotator in polygon_annotators.items():
        annotator.annotate(scene=frame, label=zone_name)

    for coords in zone_coords.values():
        for pt in coords:
            cv2.circle(frame, tuple(pt), 5, (0, 255, 0), -1)

    return frame, positions

def mouse_callback(event, x, y, flags, param):
    global dragging, current_point
    if event == cv2.EVENT_LBUTTONDOWN:
        for zone_name, coords in zone_coords.items():
            for i, pt in enumerate(coords):
                if np.linalg.norm(pt - [x, y]) < 10:
                    current_point = (zone_name, i)
                    dragging = True
                    break
    elif event == cv2.EVENT_MOUSEMOVE:
        if dragging:
            if isinstance(current_point[0], str):
                zone_coords[current_point[0]][current_point[1]] = [x, y]
    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False
        current_point = None
        # Save updated zones to JSON
        save_zones()

def in_out():
    model = YOLO('/home/manavis/yolov8s.pt')
    
    cap = cv2.VideoCapture(rtsp_link)

    if not cap.isOpened():
        print("Error: Unable to open video stream.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    video_writer, video_filename = start_new_video_recording(cap, frame_width, frame_height)
    video_start_time = datetime.now()
    
    box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    client = init_mongodb()

    latest_zone_counts = get_latest_counts(client)
    
    for zone_name in zone_coords.keys():
        zone_cumulative_counts[zone_name] = latest_zone_counts.get(zone_name, 0)

    global current_positions
    current_positions = {}
    entry_times = {}
    track_history = {}

    cv2.namedWindow('Customer Detection')
    cv2.setMouseCallback('Customer Detection', mouse_callback)

    previous_rtsp_link = rtsp_link  # Keep track of the previous RTSP link

    try:
        while True:
            reload_env_file_if_modified()
            reload_zones_file_if_modified()  # Check for changes in the zones file

            # Check if the RTSP link has changed
            if rtsp_link != previous_rtsp_link:
                print(f"Detected change in RTSP link. Previous: {previous_rtsp_link}, New: {rtsp_link}")
                
                # Release the old video capture object
                cap.release()
                
                # Initialize a new video capture object with the updated RTSP link
                cap = cv2.VideoCapture(rtsp_link)
                if not cap.isOpened():
                    print("Error: Unable to open new video stream.")
                    break

                # Update the video writer
                frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                video_writer.release()  # Release the old video writer
                video_writer, video_filename = start_new_video_recording(cap, frame_width, frame_height)
                video_start_time = datetime.now()
                
                previous_rtsp_link = rtsp_link  # Update the previous link

            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to retrieve frame from video stream.")
                break
            
            # Resize the frame if needed (for consistency with the VideoWriter resolution)
            frame = cv2.resize(frame, (640, 360))
            
            results = model.track(source=frame, tracker="bytetrack.yaml", stream=True, classes=0, persist=True)
            for result in results:
                if hasattr(result, 'boxes') and result.boxes is not None:
                    detections = sv.Detections.from_ultralytics(result)
                    if result.boxes.id is not None:
                        detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)
            
                    frame, positions = process_frame(frame, detections, box_annotator, model, label_annotator)

            # Write the frame to the video file
            video_writer.write(frame)

            # Check if 30 minutes have passed to start a new video file
            if datetime.now() - video_start_time >= timedelta(minutes=30):
                video_writer.release()
                video_writer, video_filename = start_new_video_recording(cap, frame_width, frame_height)
                video_start_time = datetime.now()
                print(f"Started new video recording: {video_filename}")

            current_ids = set(detections.tracker_id if detections.tracker_id is not None else [])
            all_tracked_ids = set(current_positions.keys())

            disappeared_ids = all_tracked_ids - current_ids

            for id in disappeared_ids:
                if id in entry_times:
                    if current_positions[id] != "None":
                        dwell_time = time.time() - entry_times[id]
                        log_to_db(client, id, current_positions[id], dwell_time=dwell_time)
                    del current_positions[id]
                    del entry_times[id]

            for idx, id in enumerate(current_ids):
                id = int(id)
                class_id = int(detections[idx].class_id[0])
                position = positions[id]

                if id not in current_positions:
                    current_positions[id] = position
                    entry_times[id] = time.time()
                    log_to_db(client, id, position, dwell_time=0)

                    track_history[id] = []

                elif current_positions[id] != position:
                    if id in entry_times:
                        if current_positions[id] != "None":
                            dwell_time = time.time() - entry_times[id]
                            log_to_db(client, id, current_positions[id], dwell_time=dwell_time)

                    current_positions[id] = position
                    entry_times[id] = time.time()
                    log_to_db(client, id, position, dwell_time=0)

                if id not in track_history:
                    track_history[id] = []
                box = detections[idx].xyxy[0]
                center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
                track_history[id].append(center)
                if len(track_history[id]) > 2:
                    track_history[id].pop(0)
                    
            cv2.imshow('Customer Detection', frame)
            if cv2.waitKey(1) == ord('q'):
                break
    finally:
        # Ensure dwell time is logged for all tracked IDs before quitting
        for id in list(current_positions.keys()):
            if id in entry_times:
                if current_positions[id] != "None":
                    dwell_time = time.time() - entry_times[id]
                    log_to_db(client, id, current_positions[id], dwell_time)

        # Release video writer and close all windows
        cap.release()
        video_writer.release()  # Save the video to the file
        cv2.destroyAllWindows()
        client.close()

if __name__ == '__main__':
    in_out()

#========================================================================================================================

import cv2
import numpy as np
import pymongo
import time
import json
from ultralytics import YOLO
import supervision as sv
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv(override=True)

# Store the last modification time of the .env file and zones file
last_modified_time = os.path.getmtime('.env')
last_zones_modified_time = os.path.getmtime(os.getenv("ZONES_FILE"))

# Load environment variables
rtsp_link = os.getenv("RTSP_LINK")
mongo_uri = os.getenv("MONGO_URI")
zones_file = os.getenv("ZONES_FILE")
mydb_name = os.getenv("MYDB")
mycol_name = os.getenv("MYCOL")

# Global variables for draggable points
dragging = False
current_point = None

# Global variables for cumulative zone counts
zone_cumulative_counts = {}

def reload_env_file_if_modified():
    global last_modified_time

    # Check if the file modification time has changed
    current_modified_time = os.path.getmtime('.env')
    if current_modified_time != last_modified_time:
        # Reload the .env file
        load_dotenv(override=True)

        # Update the global variables with the new values
        global rtsp_link, mongo_uri, zones_file, mydb_name, mycol_name
        rtsp_link = os.getenv("RTSP_LINK")
        mongo_uri = os.getenv("MONGO_URI")
        zones_file = os.getenv("ZONES_FILE")
        mydb_name = os.getenv("MYDB")
        mycol_name = os.getenv("MYCOL")

        # Update the modification time
        last_modified_time = current_modified_time

def reload_zones_file_if_modified():
    global last_zones_modified_time, zone_coords

    # Check if the zones file modification time has changed
    current_zones_modified_time = os.path.getmtime(zones_file)
    if current_zones_modified_time != last_zones_modified_time:
        # Reload the zones file
        zone_coords = load_zones()

        # Update the modification time
        last_zones_modified_time = current_zones_modified_time
        print("Zones file reloaded.")

def load_zones():
    with open(zones_file, 'r') as f:
        zones = json.load(f)
    # Dynamically load zones
    return {zone_name: np.array(zone, np.int32) for zone_name, zone in zones['zones'].items()}

def save_zones():
    zones = {zone_name: zone.tolist() for zone_name, zone in zone_coords.items()}
    with open(zones_file, 'w') as f:
        json.dump({"zones": zones}, f, indent=4)

# Load initial zone coordinates
zone_coords = load_zones()

# Initialize the global zone cumulative counts
for zone_name in zone_coords.keys():
    zone_cumulative_counts[zone_name] = 0

def init_mongodb():
    return pymongo.MongoClient(mongo_uri)

def log_to_db(client, customer_id, zone_name, dwell_time=0):
    try:
        mydb = client[mydb_name]  # Use the db name from .env
        mycol = mydb[mycol_name]  # Use the collection name from .env

        record = {
            "customer_id": int(customer_id),  # Convert to native int
            "booth_name": zone_name,
            "dwell_time": float(dwell_time),  # Ensure dwell time is a float
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Add timestamp
        }
        
        # Include the cumulative counts for each zone dynamically
        for zone_name, count in zone_cumulative_counts.items():
            record[f"{zone_name}_Count"] = int(count)  # Convert to native int

        mycol.insert_one(record)
        print(f"Logged to DB: {record}")
        
    except pymongo.errors.PyMongoError as e:
        print(f"Error logging to DB: {e}")

def get_latest_counts(client):
    try:
        mydb = client[mydb_name]  # Use the db name from .env
        mycol = mydb[mycol_name]  # Use the collection name from .env

        # Get the latest zone counts from the DB
        latest_zone_counts = {zone_name: 0 for zone_name in zone_coords.keys()}

        # Query for the latest zone counts
        latest_record = mycol.find_one({}, sort=[("_id", pymongo.DESCENDING)])

        if latest_record:
            # Extract zone counts
            for zone_name in latest_zone_counts.keys():
                if f"{zone_name}_Count" in latest_record:
                    latest_zone_counts[zone_name] = latest_record[f"{zone_name}_Count"]

        return latest_zone_counts

    except pymongo.errors.PyMongoError as e:
        print(f"Error fetching latest counts from DB: {e}")
        return {}

# Initialize the global visited_zones dictionary
visited_zones = {}

# Function to start video recording
def start_new_video_recording(cap, frame_width, frame_height):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_filename = f"/app/output/output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    video_writer = cv2.VideoWriter(video_filename, fourcc, 25, (frame_width, frame_height))
    return video_writer, video_filename

def process_frame(frame, detections, box_annotator, model, label_annotator):
    reload_zones_file_if_modified()  # Check for changes in zones file

    positions = {}
    polygon_zones = {zone_name: sv.PolygonZone(polygon=coords, triggering_anchors=[sv.Position.CENTER]) 
                     for zone_name, coords in zone_coords.items()}
    polygon_annotators = {zone_name: sv.PolygonZoneAnnotator(zone=polygon_zone, color=color)
                          for zone_name, (polygon_zone, color) in zip(polygon_zones.keys(), zip(polygon_zones.values(), [sv.Color.GREEN, sv.Color.RED, sv.Color.BLUE]))}

    for i, (xyxy, mask, confidence, class_id, tracker_id, data) in enumerate(detections):
        position = "None"
        for zone_name, polygon_zone in polygon_zones.items():
            if polygon_zone.trigger(detections=detections)[i]:
                position = zone_name  # Dynamically use zone name
                
                # Check if this tracker_id has visited the zone before
                if tracker_id not in visited_zones:
                    visited_zones[tracker_id] = set()  # Initialize visited zones for this tracker_id
                
                if zone_name not in visited_zones[tracker_id]:
                    # First time entering this zone
                    zone_cumulative_counts[zone_name] += 1
                    visited_zones[tracker_id].add(zone_name)  # Mark the zone as visited
                    print(f"Zone {zone_name} count: {zone_cumulative_counts[zone_name]}")
                
                # Update the current position for this tracker_id
                current_positions[tracker_id] = zone_name
                break
        
        positions[tracker_id] = position

    frame = box_annotator.annotate(scene=frame, detections=detections)
    frame = label_annotator.annotate(scene=frame, detections=detections)
    
    for zone_name, annotator in polygon_annotators.items():
        annotator.annotate(scene=frame, label=zone_name)

    for coords in zone_coords.values():
        for pt in coords:
            cv2.circle(frame, tuple(pt), 5, (0, 255, 0), -1)

    return frame, positions

def mouse_callback(event, x, y, flags, param):
    global dragging, current_point
    if event == cv2.EVENT_LBUTTONDOWN:
        for zone_name, coords in zone_coords.items():
            for i, pt in enumerate(coords):
                if np.linalg.norm(pt - [x, y]) < 10:
                    current_point = (zone_name, i)
                    dragging = True
                    break
    elif event == cv2.EVENT_MOUSEMOVE:
        if dragging:
            if isinstance(current_point[0], str):
                zone_coords[current_point[0]][current_point[1]] = [x, y]
    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False
        current_point = None
        # Save updated zones to JSON
        save_zones()

def in_out():
    model = YOLO('/home/manavis/yolov8s.pt')
    
    cap = cv2.VideoCapture(rtsp_link)

    if not cap.isOpened():
        print("Error: Unable to open video stream.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    video_writer, video_filename = start_new_video_recording(cap, frame_width, frame_height)
    video_start_time = datetime.now()
    
    box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    client = init_mongodb()

    latest_zone_counts = get_latest_counts(client)
    
    for zone_name in zone_coords.keys():
        zone_cumulative_counts[zone_name] = latest_zone_counts.get(zone_name, 0)

    global current_positions
    current_positions = {}
    entry_times = {}
    track_history = {}

    cv2.namedWindow('Customer Detection')
    cv2.setMouseCallback('Customer Detection', mouse_callback)

    previous_rtsp_link = rtsp_link  # Keep track of the previous RTSP link

    try:
        while True:
            reload_env_file_if_modified()
            reload_zones_file_if_modified()  # Check for changes in the zones file

            # Check if the RTSP link has changed
            if rtsp_link != previous_rtsp_link:
                print(f"Detected change in RTSP link. Previous: {previous_rtsp_link}, New: {rtsp_link}")
                
                # Release the old video capture object
                cap.release()
                
                # Initialize a new video capture object with the updated RTSP link
                cap = cv2.VideoCapture(rtsp_link)
                if not cap.isOpened():
                    print("Error: Unable to open new video stream.")
                    break

                # Update the video writer
                frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                video_writer.release()  # Release the old video writer
                video_writer, video_filename = start_new_video_recording(cap, frame_width, frame_height)
                video_start_time = datetime.now()
                
                previous_rtsp_link = rtsp_link  # Update the previous link

            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to retrieve frame from video stream.")
                break
            
            # Resize the frame if needed (for consistency with the VideoWriter resolution)
            frame = cv2.resize(frame, (640, 360))
            
            results = model.track(source=frame, tracker="bytetrack.yaml", stream=True, classes=0, persist=True)
            for result in results:
                if hasattr(result, 'boxes') and result.boxes is not None:
                    detections = sv.Detections.from_ultralytics(result)
                    if result.boxes.id is not None:
                        detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)
            
                    frame, positions = process_frame(frame, detections, box_annotator, model, label_annotator)

            # Write the frame to the video file
            video_writer.write(frame)

            # Check if 30 minutes have passed to start a new video file
            if datetime.now() - video_start_time >= timedelta(minutes=30):
                video_writer.release()
                video_writer, video_filename = start_new_video_recording(cap, frame_width, frame_height)
                video_start_time = datetime.now()
                print(f"Started new video recording: {video_filename}")

            current_ids = set(detections.tracker_id if detections.tracker_id is not None else [])
            all_tracked_ids = set(current_positions.keys())

            disappeared_ids = all_tracked_ids - current_ids

            for id in disappeared_ids:
                if id in entry_times:
                    if current_positions[id] != "None":
                        dwell_time = time.time() - entry_times[id]
                        log_to_db(client, id, current_positions[id], dwell_time=dwell_time)
                    del current_positions[id]
                    del entry_times[id]

            for idx, id in enumerate(current_ids):
                id = int(id)
                class_id = int(detections[idx].class_id[0])
                position = positions[id]

                if id not in current_positions:
                    current_positions[id] = position
                    entry_times[id] = time.time()
                    log_to_db(client, id, position, dwell_time=0)

                    track_history[id] = []

                elif current_positions[id] != position:
                    if id in entry_times:
                        if current_positions[id] != "None":
                            dwell_time = time.time() - entry_times[id]
                            log_to_db(client, id, current_positions[id], dwell_time=dwell_time)

                    current_positions[id] = position
                    entry_times[id] = time.time()
                    log_to_db(client, id, position, dwell_time=0)

                if id not in track_history:
                    track_history[id] = []
                box = detections[idx].xyxy[0]
                center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
                track_history[id].append(center)
                if len(track_history[id]) > 2:
                    track_history[id].pop(0)
                    
            cv2.imshow('Customer Detection', frame)
            if cv2.waitKey(1) == ord('q'):
                break
    finally:
        # Ensure dwell time is logged for all tracked IDs before quitting
        for id in list(current_positions.keys()):
            if id in entry_times:
                if current_positions[id] != "None":
                    dwell_time = time.time() - entry_times[id]
                    log_to_db(client, id, current_positions[id], dwell_time)

        # Release video writer and close all windows
        cap.release()
        video_writer.release()  # Save the video to the file
        cv2.destroyAllWindows()
        client.close()

if __name__ == '__main__':
    in_out()

