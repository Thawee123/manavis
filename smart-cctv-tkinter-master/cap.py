import cv2

def load_env_file():
    """Load the .env file and return the RTSP link."""
    rtsp_link = None
    try:
        with open('.env', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip():  # Ignore empty lines
                    key, value = line.strip().split('=', 1)
                    if key == "RTSP_LINK":
                        rtsp_link = value.strip()  # Store RTSP link
                        break  # No need to continue once we found the RTSP link
    except FileNotFoundError:
        print("No .env file found.")
    return rtsp_link  # Return the RTSP link

def cap_pic():
    # Replace with your RTSP stream URL
    rtsp_url = load_env_file()

    # Open the RTSP stream
    if rtsp_url.isdigit():
        cap = cv2.VideoCapture(int(rtsp_url))
    else:
        cap = cv2.VideoCapture(rtsp_url)
    # cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Failed to open RTSP stream")
        exit()

    frame_count = 0

    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        

    # Display the frame
    cv2.imshow('RTSP Stream', frame)

    # Save frame as an image (optional)
    frame_count += 1
    frame_filename = f"frame_1.jpg"
    cv2.imwrite(frame_filename, frame)
        


    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()
