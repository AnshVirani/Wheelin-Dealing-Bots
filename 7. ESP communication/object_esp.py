import cv2 as cv
from cv2 import aruco
import numpy as np
import math
import requests
import tkinter as tk
from threading import Thread


# ESP32 Configuration
ESP32_IP = "192.168.137.8"  # Replace with your ESP32's IP address


# Load in the calibration data
calib_data = np.load(r"C:\Users\viran\Downloads\OpenCV-main\Wheelin-Dealing-Bots\4. calib_data\MultiMatrix.npz")


# Extract the camera calibration matrices
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]


MARKER_SIZE = 6  # Size of the markers in cm


# Define the known coordinates of each corner marker
marker_coords = {
    0: (0, 0),      # Marker 0 at (0, 0)
    1: (150, 0),    # Marker 1 at (150, 0)
    2: (150, -60),  # Marker 2 at (150, -60)
    3: (0, -60),    # Marker 3 at (0, -60)
}


# Define marker IDs for the robot and the object
ROBOT_MARKER_ID = 4
OBJECT_MARKER_ID = 5


# Define the dictionary for ArUco markers
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
param_markers = aruco.DetectorParameters()


# Function to map marker positions to real-world coordinates
def get_real_world_coordinates(tVec, H):
    point_camera = np.array([tVec[0][0], tVec[0][1], 1.0])  # (x, y, 1) in the camera frame
    point_world = np.dot(H, point_camera.T)  # Transform to the world frame
    return point_world[0] / point_world[2], point_world[1] / point_world[2]  # Normalize by z


# Function to send coordinates to ESP32
def send_coordinates_to_esp(robot_position, object_position):
    try:
        response = requests.get(
            f"http://{ESP32_IP}/set_coordinates",
            params={
                "robotX": robot_position[0],
                "robotY": robot_position[1],
                "objectX": object_position[0],
                "objectY": object_position[1],
            },
        )
        if response.status_code == 200:
            print("Coordinates sent successfully!")
        else:
            print(f"Failed to send coordinates: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending coordinates to ESP32: {e}")


# Function to track and send coordinates
def track_and_send():
    cap = cv.VideoCapture(0)
    robot_position = None
    object_position = None
    homography_matrix = None


    while True:
        ret, frame = cap.read()
        if not ret:
            break


        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        marker_corners, marker_IDs, _ = aruco.detectMarkers(
            gray_frame, marker_dict, parameters=param_markers
        )


        if marker_corners:
            rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
                marker_corners, MARKER_SIZE, cam_mat, dist_coef
            )


            camera_points = []
            world_points = []


            for i, (ids, corners) in enumerate(zip(marker_IDs, marker_corners)):
                marker_id = ids[0]


                if marker_id in marker_coords:
                    camera_points.append([tVec[i][0][0], tVec[i][0][1]])
                    world_points.append(marker_coords[marker_id])


            if len(camera_points) == 4:
                camera_points = np.array(camera_points, dtype=np.float32)
                world_points = np.array(world_points, dtype=np.float32)
                homography_matrix, _ = cv.findHomography(camera_points, world_points)


            for i, (ids, corners) in enumerate(zip(marker_IDs, marker_corners)):
                marker_id = ids[0]


                if marker_id == ROBOT_MARKER_ID and homography_matrix is not None:
                    robot_position = get_real_world_coordinates(tVec[i], homography_matrix)


                if marker_id == OBJECT_MARKER_ID and homography_matrix is not None:
                    object_position = get_real_world_coordinates(tVec[i], homography_matrix)


        if robot_position and object_position:
            print(f"Robot Position: {robot_position}, Object Position: {object_position}")
            send_coordinates_to_esp(robot_position, object_position)
            break


        cv.imshow("Robot and Object Tracking", frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break


    cap.release()
    cv.destroyAllWindows()


# Function to launch tracking in a separate thread
def start_tracking():
    tracking_thread = Thread(target=track_and_send, daemon=True)
    tracking_thread.start()


# GUI for Start Button
def create_gui():
    root = tk.Tk()
    root.title("Robot and Object Tracker")


    tk.Label(root, text="Robot and Object Tracking", font=("Arial", 16)).pack(pady=10)


    start_button = tk.Button(
        root,
        text="Start",
        font=("Arial", 14),
        bg="green",
        fg="white",
        command=start_tracking
    )
    start_button.pack(pady=20)


    root.mainloop()


# Run the GUI
if __name__ == "__main__":
    create_gui()