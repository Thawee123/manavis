# import cv2
# import numpy as np
# import json
# import os
# import argparse
# from dotenv import load_dotenv

# # Global variables for draggable points
# dragging = False
# current_point = None

# # Load environment variables from .env file
# load_dotenv(override=True)

# # Store the last modification time of the .env file
# last_modified_time = os.path.getmtime('.env')

# # Load environment variables
# rtsp_link = os.getenv("RTSP_LINK")

# def reload_env_file_if_modified():
#     global last_modified_time

#     # Check if the file modification time has changed
#     current_modified_time = os.path.getmtime('.env')
#     if current_modified_time != last_modified_time:
#         load_dotenv(override=True)
#         global rtsp_link, mongo_uri, zones_file, mydb_name, mycol_name
#         rtsp_link = os.getenv("RTSP_LINK")
#         mongo_uri = os.getenv("MONGO_URI")
#         zones_file = os.getenv("ZONES_FILE")
#         mydb_name = os.getenv("MYDB")
#         mycol_name = os.getenv("MYCOL")
#         last_modified_time = current_modified_time

# # Base path for your project
# base_path = r'D:\VSCode\gui\smart-cctv-tkinter-master\zonejson'

# # Default coordinates for zones
# default_zones = {
#     "Entrance": [[20, 100], [20, 20], [100, 20], [100, 100]],
#     "Pawn Zone": [[120, 20], [190, 20], [190, 80], [120, 80]],
#     "Waiting Zone": [[220, 60], [320, 60], [320, 120], [220, 120]],
#     "Shop Zone": [[40, 170], [100, 170], [100, 120], [40, 120]],
#     "Cashier Zone": [[40, 280], [120, 280], [120, 200], [40, 200]],
#     "Storage Zone": [[130, 170], [200, 170], [200, 120], [130, 120]],
#     "Exit Zone": [[300, 20], [370, 20], [370, 80], [300, 80]],
#     "Customer Service Zone": [[250, 150], [320, 150], [320, 200], [250, 200]],
#     "Display Zone": [[20, 320], [100, 320], [100, 400], [20, 400]],
#     "Staff Area": [[140, 300], [200, 300], [200, 350], [140, 350]],
#     "Break Room": [[220, 250], [300, 250], [300, 320], [220, 320]],
#     "Manager Zone": [[330, 150], [400, 150], [400, 200], [330, 200]],
#     "Inventory Zone": [[50, 420], [120, 420], [120, 480], [50, 480]],
#     "Check-out Zone": [[180, 380], [250, 380], [250, 450], [180, 450]],
#     "Reception Zone": [[260, 400], [330, 400], [330, 460], [260, 460]]
# }

# # Load zones from file or initialize with default coordinates for new names
# def load_zones(zones_file, user_zone_names):
#     default_zone_names = list(default_zones.keys())
#     zone_coords = {}

#     for i, user_name in enumerate(user_zone_names):
#         # Assign default coordinates if available, otherwise create an empty zone
#         if i < len(default_zone_names):
#             zone_coords[user_name] = np.array(default_zones[default_zone_names[i]], np.int32)
#         else:
#             zone_coords[user_name] = np.array([], np.int32)  # Create an empty zone if more zones than defaults

#     # Update coordinates for zones from the JSON file, if it exists
#     if os.path.exists(zones_file):
#         with open(zones_file, 'r') as f:
#             existing_zones = json.load(f).get("zones", {})
#             for name, coords in existing_zones.items():
#                 if name in zone_coords:
#                     zone_coords[name] = np.array(coords, np.int32)

#     return zone_coords

# # Save zones to file
# def save_zones(zones_file, zone_coords):
#     zones = {zone_name: zone.tolist() for zone_name, zone in zone_coords.items()}
#     with open(zones_file, 'w') as f:
#         json.dump({"zones": zones}, f, indent=4)

# # Handle mouse events for dragging points
# def mouse_callback(event, x, y, flags, param):
#     global dragging, current_point
#     zone_coords, zones_file = param  # Unpack parameters

#     if event == cv2.EVENT_LBUTTONDOWN:
#         for zone_name, coords in zone_coords.items():
#             if len(coords) > 0:  # Only check zones with points
#                 for i, pt in enumerate(coords):
#                     if np.linalg.norm(pt - [x, y]) < 10:
#                         current_point = (zone_name, i)
#                         dragging = True
#                         break
#     elif event == cv2.EVENT_MOUSEMOVE:
#         if dragging:
#             zone_coords[current_point[0]][current_point[1]] = [x, y]
#     elif event == cv2.EVENT_LBUTTONUP:
#         dragging = False
#         current_point = None
#         # Save updated zones to JSON
#         save_zones(zones_file, zone_coords)

# def load_env(camera_choice):
#     env_path = os.path.join(base_path, camera_choice.capitalize(), '.env')

#     if os.path.exists(env_path):
#         load_dotenv(dotenv_path=env_path)
#     else:
#         print(f"Warning: .env file not found at {env_path}. Continuing without environment variables.")

# def rect_noise(camera_choice):
#     global zone_count

#     # Load environment variables based on the camera choice
#     load_env(camera_choice)

#     # Check if it's an integer for webcam usage
#     if rtsp_link.isdigit():
#         cap = cv2.VideoCapture(int(rtsp_link))
#     else:
#         cap = cv2.VideoCapture(rtsp_link)

#     if not cap.isOpened():
#         print("Error: Unable to open video stream.")
#         return

#     # Set zones file path
#     zones_file = os.path.join(base_path, 'easymoneyzone.json')

#     # Ask user for number of zones to create and prompt for each zone name
#     zone_count = int(input("Enter the number of zones to create: "))
#     zone_names = []
#     for i in range(zone_count):
#         zone_name = input(f"Enter name for zone {i + 1}: ")
#         zone_names.append(zone_name)

#     # Load zones, starting with default zones or empty coordinates for new zones
#     zone_coords = load_zones(zones_file, zone_names)

#     cv2.namedWindow('Zone Editor')
#     cv2.setMouseCallback('Zone Editor', mouse_callback, param=(zone_coords, zones_file))

#     previous_rtsp_link = rtsp_link

#     try:
#         zone_index = 0

#         while zone_index < zone_count:
#             reload_env_file_if_modified()

#             # Check if the RTSP link has changed
#             if rtsp_link != previous_rtsp_link:
#                 print(f"Detected change in RTSP link. Previous: {previous_rtsp_link}, New: {rtsp_link}")
#                 cap.release()
#                 if rtsp_link.isdigit():
#                     cap = cv2.VideoCapture(int(rtsp_link))
#                 else:
#                     cap = cv2.VideoCapture(rtsp_link)

#                 if not cap.isOpened():
#                     print("Error: Unable to open new video stream.")
#                     break
#                 previous_rtsp_link = rtsp_link

#             ret, frame = cap.read()
#             if not ret:
#                 print("Error: Unable to retrieve frame from video stream.")
#                 break

#             # Draw existing zones with default or loaded coordinates
#             for zone_name, coords in zone_coords.items():
#                 if len(coords) > 0:  # Only draw non-empty zones
#                     cv2.polylines(frame, [coords], isClosed=True, color=(0, 255, 0), thickness=2)
#                     for pt in coords:
#                         cv2.circle(frame, tuple(pt), 5, (0, 255, 0), -1)
#                     cv2.putText(frame, zone_name, tuple(coords[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

#             # Draw the current zone for adjustment
#             zone_name = zone_names[zone_index]
#             cv2.putText(frame, f"Adjust Zone: {zone_name} (Press 'n' to finalize)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

#             # Display the frame
#             cv2.imshow('Zone Editor', frame)

#             # Press 'n' to finalize adjustments and move to the next zone
#             key = cv2.waitKey(1)
#             if key == ord('n'):
#                 # Save the adjusted zone to JSON
#                 zone_coords[zone_name] = np.array(zone_coords[zone_name], np.int32)
#                 zone_index += 1
#                 save_zones(zones_file, zone_coords)

#             # Press 'q' to quit
#             elif key == ord('q'):
#                 break

#     finally:
#         cap.release()
#         cv2.destroyAllWindows()

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description="Zone drawing tool for multiple cameras.")
#     parser.add_argument('camera', choices=['entrance', 'store'], help="Specify the camera to draw zones on.", nargs='?', default='entrance')
#     args = parser.parse_args()
#     rect_noise(args.camera)

##version2 is have popup already but not link with main page
# import cv2
# import numpy as np
# import json
# import os
# import argparse
# from dotenv import load_dotenv
# import tkinter as tk
# from tkinter import messagebox

# # Base path for your project
# base_path = r'D:\VSCode\gui\smart-cctv-tkinter-master\zonejson'

# # Global variables for draggable points
# dragging = False
# current_point = None

# # Load environment variables from .env file
# load_dotenv(override=True)

# # Store the last modification time of the .env file
# last_modified_time = os.path.getmtime('.env')

# # Load environment variables
# rtsp_link = os.getenv("RTSP_LINK")

# # Default coordinates for zones
# default_zones = {
#     "Entrance": [[20, 100], [20, 20], [100, 20], [100, 100]],
#     "Pawn Zone": [[120, 20], [190, 20], [190, 80], [120, 80]],
#     "Waiting Zone": [[220, 60], [320, 60], [320, 120], [220, 120]],
#     "Shop Zone": [[40, 170], [100, 170], [100, 120], [40, 120]],
#     "Cashier Zone": [[40, 280], [120, 280], [120, 200], [40, 200]],
#     "Storage Zone": [[130, 170], [200, 170], [200, 120], [130, 120]],
#     "Exit Zone": [[300, 20], [370, 20], [370, 80], [300, 80]],
#     "Customer Service Zone": [[250, 150], [320, 150], [320, 200], [250, 200]],
#     "Display Zone": [[20, 320], [100, 320], [100, 400], [20, 400]],
#     "Staff Area": [[140, 300], [200, 300], [200, 350], [140, 350]],
#     "Break Room": [[220, 250], [300, 250], [300, 320], [220, 320]],
#     "Manager Zone": [[330, 150], [400, 150], [400, 200], [330, 200]],
#     "Inventory Zone": [[50, 420], [120, 420], [120, 480], [50, 480]],
#     "Check-out Zone": [[180, 380], [250, 380], [250, 450], [180, 450]],
#     "Reception Zone": [[260, 400], [330, 400], [330, 460], [260, 460]]
# }

# # Tkinter window to collect the number of zones and their names
# class ZoneConfigGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Zone Configuration")

#         # Label and entry for the number of zones
#         self.zone_count_label = tk.Label(root, text="Enter the number of zones:")
#         self.zone_count_label.pack()
#         self.zone_count_entry = tk.Entry(root)
#         self.zone_count_entry.pack()

#         # Button to confirm the number of zones
#         self.confirm_button = tk.Button(root, text="Confirm", command=self.add_zone_entries)
#         self.confirm_button.pack()

#         self.zone_name_entries = []
#         self.start_button = None

#     def add_zone_entries(self):
#         try:
#             self.zone_count = int(self.zone_count_entry.get())
#             if self.zone_count < 1:
#                 raise ValueError("Number of zones must be at least 1")

#             # Create entry fields for each zone name
#             tk.Label(self.root, text="Enter the names for each zone:").pack()
#             for i in range(self.zone_count):
#                 zone_name_label = tk.Label(self.root, text=f"Zone {i+1} Name:")
#                 zone_name_label.pack()
#                 zone_name_entry = tk.Entry(self.root)
#                 zone_name_entry.pack()
#                 self.zone_name_entries.append(zone_name_entry)

#             # Button to start the zone drawing
#             self.start_button = tk.Button(self.root, text="Start Zone Drawing", command=self.start_zone_drawing)
#             self.start_button.pack()
#         except ValueError as e:
#             messagebox.showerror("Input Error", str(e))

#     def start_zone_drawing(self):
#         # Get all zone names from the entries
#         zone_names = [entry.get() for entry in self.zone_name_entries]
#         if any(not name for name in zone_names):
#             messagebox.showerror("Input Error", "All zone names must be filled in.")
#             return

#         self.root.destroy()  # Close the GUI window
#         rect_noise(zone_names)  # Start zone drawing

# # Load zones from file or initialize with default coordinates for new names
# def load_zones(zones_file, user_zone_names):
#     default_zone_names = list(default_zones.keys())
#     zone_coords = {}

#     for i, user_name in enumerate(user_zone_names):
#         # Assign default coordinates if available, otherwise create an empty zone
#         if i < len(default_zone_names):
#             zone_coords[user_name] = np.array(default_zones[default_zone_names[i]], np.int32)
#         else:
#             zone_coords[user_name] = np.array([], np.int32)  # Create an empty zone if more zones than defaults

#     # Update coordinates for zones from the JSON file, if it exists
#     if os.path.exists(zones_file):
#         with open(zones_file, 'r') as f:
#             existing_zones = json.load(f).get("zones", {})
#             for name, coords in existing_zones.items():
#                 if name in zone_coords:
#                     zone_coords[name] = np.array(coords, np.int32)

#     return zone_coords

# # Save zones to file
# def save_zones(zones_file, zone_coords):
#     zones = {zone_name: zone.tolist() for zone_name, zone in zone_coords.items()}
#     with open(zones_file, 'w') as f:
#         json.dump({"zones": zones}, f, indent=4)

# # Handle mouse events for dragging points
# def mouse_callback(event, x, y, flags, param):
#     global dragging, current_point
#     zone_coords, zones_file = param  # Unpack parameters

#     if event == cv2.EVENT_LBUTTONDOWN:
#         for zone_name, coords in zone_coords.items():
#             if len(coords) > 0:  # Only check zones with points
#                 for i, pt in enumerate(coords):
#                     if np.linalg.norm(pt - [x, y]) < 10:
#                         current_point = (zone_name, i)
#                         dragging = True
#                         break
#     elif event == cv2.EVENT_MOUSEMOVE:
#         if dragging:
#             zone_coords[current_point[0]][current_point[1]] = [x, y]
#     elif event == cv2.EVENT_LBUTTONUP:
#         dragging = False
#         current_point = None
#         # Save updated zones to JSON
#         save_zones(zones_file, zone_coords)

# def rect_noise(zone_names):
#     # Set zones file path
#     zones_file = os.path.join(base_path, 'easymoneyzone.json')

#     # Load zones, starting with default zones or empty coordinates for new zones
#     zone_coords = load_zones(zones_file, zone_names)

#     cv2.namedWindow('Zone Editor')
#     cv2.setMouseCallback('Zone Editor', mouse_callback, param=(zone_coords, zones_file))

#     # Initialize video capture
#     if rtsp_link.isdigit():
#         cap = cv2.VideoCapture(int(rtsp_link))
#     else:
#         cap = cv2.VideoCapture(rtsp_link)

#     if not cap.isOpened():
#         print("Error: Unable to open video stream.")
#         return

#     try:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 print("Error: Unable to retrieve frame from video stream.")
#                 break

#             # Draw existing zones
#             for zone_name, coords in zone_coords.items():
#                 if len(coords) > 0:
#                     cv2.polylines(frame, [coords], isClosed=True, color=(0, 255, 0), thickness=2)
#                     for pt in coords:
#                         cv2.circle(frame, tuple(pt), 5, (0, 255, 0), -1)
#                     cv2.putText(frame, zone_name, tuple(coords[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

#             # Display the frame
#             cv2.imshow('Zone Editor', frame)

#             # Press 'q' to quit
#             if cv2.waitKey(1) == ord('q'):
#                 break
#     finally:
#         cap.release()
#         cv2.destroyAllWindows()

# if __name__ == '__main__':
#     # Initialize Tkinter GUI
#     root = tk.Tk()
#     app = ZoneConfigGUI(root)
#     root.mainloop()

import cv2
import numpy as np
import json
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from dotenv import load_dotenv

# Global variables for draggable points
dragging = False
current_point = None

# Load environment variables from .env file
load_dotenv(override=True)

# Load environment variables
rtsp_link = os.getenv("RTSP_LINK")

# Base path for your project
base_path = r'D:\VSCode\gui\smart-cctv-tkinter-master\zonejson'

# Default coordinates for zones
default_zones = {
    "Entrance": [[20, 100], [20, 20], [100, 20], [100, 100]],
    "Pawn Zone": [[120, 20], [190, 20], [190, 80], [120, 80]],
    "Waiting Zone": [[220, 60], [320, 60], [320, 120], [220, 120]],
    "Shop Zone": [[40, 170], [100, 170], [100, 120], [40, 120]],
    "Cashier Zone": [[40, 280], [120, 280], [120, 200], [40, 200]],
    "Storage Zone": [[130, 170], [200, 170], [200, 120], [130, 120]],
    "Exit Zone": [[300, 20], [370, 20], [370, 80], [300, 80]],
    "Customer Service Zone": [[250, 150], [320, 150], [320, 200], [250, 200]],
    "Display Zone": [[20, 320], [100, 320], [100, 400], [20, 400]],
    "Staff Area": [[140, 300], [200, 300], [200, 350], [140, 350]],
    "Break Room": [[220, 250], [300, 250], [300, 320], [220, 320]],
    "Manager Zone": [[330, 150], [400, 150], [400, 200], [330, 200]],
    "Inventory Zone": [[50, 420], [120, 420], [120, 480], [50, 480]],
    "Check-out Zone": [[180, 380], [250, 380], [250, 450], [180, 450]],
    "Reception Zone": [[260, 400], [330, 400], [330, 460], [260, 460]]
}

# Load zones from file or initialize with default coordinates for new names
def load_zones(zones_file, user_zone_names):
    default_zone_names = list(default_zones.keys())
    zone_coords = {}

    for i, user_name in enumerate(user_zone_names):
        if i < len(default_zone_names):  # Use default coordinates if available
            zone_coords[user_name] = np.array(default_zones[default_zone_names[i]], np.int32)
        else:
            zone_coords[user_name] = np.array([], np.int32)  # Empty zone if more zones than defaults

    # Update coordinates for zones from the JSON file, if it exists
    if os.path.exists(zones_file):
        with open(zones_file, 'r') as f:
            existing_zones = json.load(f).get("zones", {})
            for name, coords in existing_zones.items():
                if name in zone_coords:
                    zone_coords[name] = np.array(coords, np.int32)

    return zone_coords

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
            if len(coords) > 0:  # Only check zones with points
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
        save_zones(zones_file, zone_coords)

def rect_noise(zone_names):
    zones_file = os.path.join(base_path, 'easymoneyzone.json')
    zone_coords = load_zones(zones_file, zone_names)

    cv2.namedWindow('Zone Editor')
    cv2.setMouseCallback('Zone Editor', mouse_callback, param=(zone_coords, zones_file))

    if rtsp_link.isdigit():
        cap = cv2.VideoCapture(int(rtsp_link))
    else:
        cap = cv2.VideoCapture(rtsp_link)

    if not cap.isOpened():
        print("Error: Unable to open video stream.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to retrieve frame from video stream.")
                break

            for zone_name, coords in zone_coords.items():
                if len(coords) > 0:
                    cv2.polylines(frame, [coords], isClosed=True, color=(0, 255, 0), thickness=2)
                    for pt in coords:
                        cv2.circle(frame, tuple(pt), 5, (0, 255, 0), -1)
                    cv2.putText(frame, zone_name, tuple(coords[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            cv2.imshow('Zone Editor', frame)
            if cv2.waitKey(1) == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

# Tkinter Popup to enter number of zones and their names
class ZoneConfigPopup:
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Zone Configuration")
        tk.Label(self.top, text="Enter the number of zones:").pack()

        self.zone_count_entry = tk.Entry(self.top)
        self.zone_count_entry.pack()

        self.confirm_button = tk.Button(self.top, text="Confirm", command=self.setup_zone_entries)
        self.confirm_button.pack()

        self.zone_name_entries = []
        self.zone_names = []

    def setup_zone_entries(self):
        try:
            zone_count = int(self.zone_count_entry.get())
            if zone_count < 1:
                raise ValueError("Number of zones must be at least 1")

            tk.Label(self.top, text="Enter the names for each zone:").pack()
            for i in range(zone_count):
                tk.Label(self.top, text=f"Zone {i+1} Name:").pack()
                entry = tk.Entry(self.top)
                entry.pack()
                self.zone_name_entries.append(entry)

            self.start_button = tk.Button(self.top, text="Start Zone Drawing", command=self.collect_zone_names)
            self.start_button.pack()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def collect_zone_names(self):
        self.zone_names = [entry.get() for entry in self.zone_name_entries]
        if any(not name for name in self.zone_names):
            messagebox.showerror("Input Error", "All zone names must be filled in.")
            return

        self.top.destroy()  # Close the popup window
        rect_noise(self.zone_names)  # Start zone drawing with the specified zone names

# def open_zone_config():
#     ZoneConfigPopup(root)

# # Main application setup
# root = tk.Tk()
# root.title("Smart CCTV")
# root.geometry("800x600")

# # Add a button to open the zone configuration popup
# btn2 = tk.Button(root, text="Rectangle", font=('Microsoft YaHei UI Light', 25, 'bold'), height=2, width=15,
#                  fg='orange', command=open_zone_config)
# btn2.pack(pady=20)

# root.mainloop()

def open_zone_config(parent):
    ZoneConfigPopup(parent)
