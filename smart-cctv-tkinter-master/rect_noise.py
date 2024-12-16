# import cv2 

# donel = False
# doner = False
# x1,y1,x2,y2 = 0,0,0,0


# def select(event, x, y, flag, param):
#     global x1,x2,y1,y2,donel, doner
#     if event == cv2.EVENT_LBUTTONDOWN:
#         x1,y1 = x,y 
#         donel = True
#     elif event == cv2.EVENT_RBUTTONDOWN:
#         x2,y2 = x,y
#         doner = True    
#         print(doner, donel)

# def rect_noise():

#     global x1,x2,y1,y2, donel, doner
#     cap = cv2.VideoCapture(0)

    

#     cv2.namedWindow("select_region")
#     cv2.setMouseCallback("select_region", select)

#     while True:
#         _, frame = cap.read()

#         cv2.imshow("select_region", frame)

#         if cv2.waitKey(1) == 27 or doner == True:
#             cv2.destroyAllWindows()
#             print("gone--")
#             break

#     while True:
#         _, frame1 = cap.read()
#         _, frame2 = cap.read()

#         frame1only = frame1[y1:y2, x1:x2]
#         frame2only = frame2[y1:y2, x1:x2]

#         diff = cv2.absdiff(frame2only, frame1only)
#         diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

#         diff = cv2.blur(diff, (5,5))
#         _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

#         contr, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
#         if len(contr) > 0:
#             max_cnt = max(contr, key=cv2.contourArea)
#             x,y,w,h = cv2.boundingRect(max_cnt)
#             cv2.rectangle(frame1, (x+x1, y+y1), (x+w+x1, y+h+y1), (0,255,0), 2)
#             cv2.putText(frame1, "MOTION", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)

#         else:
#             cv2.putText(frame1, "NO-MOTION", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2)

#         cv2.rectangle(frame1, (x1,y1), (x2, y2), (0,0,255), 1)
#         cv2.imshow("esc. to exit", frame1)

#         if cv2.waitKey(1) == 27:
#             cap.release()
#             cv2.destroyAllWindows()
#             break

import cv2
import numpy as np
import json
import os
import argparse
from dotenv import load_dotenv

# Global variables for draggable points
dragging = False
current_point = None

# Load environment variables from .env file
load_dotenv(override=True)

# Store the last modification time of the .env file
last_modified_time = os.path.getmtime('.env')

# Load environment variables
rtsp_link = os.getenv("RTSP_LINK")

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

# Adjusted default zone coordinates for a 640x360 frame
default_zones = {
    "Entrance": [[20, 100], [20, 20], [100, 20], [100, 100]],
    "Pawn Zone": [[120, 20], [190, 20], [190, 80], [120, 80]],
    "Waiting Zone": [[220, 60], [320, 60], [320, 120], [220, 120]],
    "Shop Zone": [[40, 170], [100, 170], [100, 120], [40, 120]],
    "Cashier Zone": [[40, 280], [120, 280], [120, 200], [40, 200]]
}

# Base path for your project
base_path = r'D:\VSCode\gui\smart-cctv-tkinter-master\zonejson'

# Load zones from file, or create a new file with default zones if not found
def load_zones(zones_file):
    if not os.path.exists(zones_file):
        print(f"Zones file '{zones_file}' not found. Creating a new one with default zones.")
        os.makedirs(os.path.dirname(zones_file), exist_ok=True)  # Create directories if they don't exist
        with open(zones_file, 'w') as f:
            json.dump({"zones": default_zones}, f, indent=4)
        return {zone_name: np.array(coords, np.int32) for zone_name, coords in default_zones.items()}

    with open(zones_file, 'r') as f:
        zones = json.load(f)
    return {zone_name: np.array(coords, np.int32) for zone_name, coords in zones['zones'].items()}

# Save zones to file
def save_zones(zones_file, zone_coords):
    zones = {zone_name: zone.tolist() for zone_name, zone in zone_coords.items()}
    with open(zones_file, 'w') as f:
        json.dump({"zones": zones}, f, indent=4)

# Handle mouse events for dragging points
def mouse_callback(event, x, y, flags, param):
    global dragging, current_point
    zone_coords, zones_file = param  # Unpack parameters

    if event == cv2.EVENT_LBUTTONDOWN:
        for zone_name, coords in zone_coords.items():
            for i, pt in enumerate(coords):
                if np.linalg.norm(pt - [x, y]) < 10:
                    current_point = (zone_name, i)
                    dragging = True
                    break
    elif event == cv2.EVENT_MOUSEMOVE:
        if dragging:
            zone_coords[current_point[0]][current_point[1]] = [x, y]
    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False
        current_point = None
        # Save updated zones to JSON
        save_zones(zones_file, zone_coords)

def load_env(camera_choice):
    # Determine .env path based on camera choice
    env_path = os.path.join(base_path, camera_choice.capitalize(), '.env')

    # Load .env file
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
    else:
        print(f"Warning: .env file not found at {env_path}. Continuing without environment variables.")

def rect_noise(camera_choice):
    # Load environment variables based on the camera choice
    load_env(camera_choice)

    # Instead of RTSP, use the webcam by setting camera index 0
    # Check if it's an integer for webcam usage
    if rtsp_link.isdigit():
        cap = cv2.VideoCapture(int(rtsp_link))
    else:
        cap = cv2.VideoCapture(rtsp_link)
    # cap = cv2.VideoCapture(rtsp_link)  # 0 for default webcam

    if not cap.isOpened():
        print("Error: Unable to open video stream.")
        return

    # Get frame dimensions
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Set zones file path in your defined directory
    zones_file = os.path.join(base_path, 'easymoneyzone2.json')

    zone_coords = load_zones(zones_file)

    # Create window and set mouse callback, pass zone_coords and zones_file as parameters
    cv2.namedWindow('Zone Editor')
    cv2.setMouseCallback('Zone Editor', mouse_callback, param=(zone_coords, zones_file))

    previous_rtsp_link = rtsp_link # Keep track of the previous RTSP link

    try:
        while True:
            reload_env_file_if_modified()

            # Check if the RTSP link has changed
            if rtsp_link != previous_rtsp_link:
                print(f"Detected change in RTSP link. Previous: {previous_rtsp_link}, New: {rtsp_link}")
                
                # Release the old video capture object
                cap.release()
                
                # Initialize a new video capture object with the updated RTSP link
                # cap = cv2.VideoCapture(rtsp_link)
                # Check if it's an integer for webcam usage
                if rtsp_link.isdigit():
                    cap = cv2.VideoCapture(int(rtsp_link))
                else:
                    cap = cv2.VideoCapture(rtsp_link)

                if not cap.isOpened():
                    print("Error: Unable to open new video stream.")
                    break

                # Update the video writer
                frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                # video_writer.release()  # Release the old video writer
                # video_writer, video_filename = start_new_video_recording(cap, frame_width, frame_height)
                # video_start_time = datetime.now()
                
                previous_rtsp_link = rtsp_link  # Update the previous link

            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to retrieve frame from video stream.")
                break

            # Draw the zones and labels on the frame
            for zone_name, coords in zone_coords.items():
                cv2.polylines(frame, [coords], isClosed=True, color=(0, 255, 0), thickness=2)
                for pt in coords:
                    cv2.circle(frame, tuple(pt), 5, (0, 255, 0), -1)
                # Display zone name near the first point
                cv2.putText(frame, zone_name, tuple(coords[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)


            # Display the frame
            cv2.imshow('Zone Editor', frame)

            # Press 'q' to quit
            if cv2.waitKey(1) == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Zone drawing tool for multiple cameras.")
    parser.add_argument('camera', choices=['entrance', 'store'], help="Specify the camera to draw zones on.", nargs='?', default='entrance')

    # Parse arguments
    args = parser.parse_args()

    # Call main function with the selected or default camera
    rect_noise(args.camera)


 
 