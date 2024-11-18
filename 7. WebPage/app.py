from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2 as cv
from cv2 import aruco
import numpy as np
import threading

# Initialize Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Load in the calibration data
calib_data = np.load(r"C:\Users\viran\Downloads\OpenCV-main\Wheelin-Dealing-Bots\4. calib_data\MultiMatrix.npz")

# Extract the camera calibration matrices
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]

MARKER_SIZE = 6  # Size of the markers in cm

# Define the known coordinates of each corner marker
marker_coords = {
    0: (0, 0),        # Marker 0 at (0, 0) - Top-left
    1: (150, 0),      # Marker 1 at (150, 0) - Top-right
    2: (150, -60),    # Marker 2 at (150, -60) - Bottom-right
    3: (0, -60),      # Marker 3 at (0, -60) - Bottom-left
}

# Define marker IDs for the robot and object
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

# Robot tracking logic
def track_robot():
    cap = cv.VideoCapture(0)
    robot_path = []
    homography_matrix = None  # Homography matrix to map camera frame to world frame

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale for marker detection
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Detect markers in the grayscale frame
        marker_corners, marker_IDs, _ = aruco.detectMarkers(gray_frame, marker_dict)

        # If markers are detected
        if marker_corners and marker_IDs is not None:
            # Estimate pose of the detected markers
            rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
                marker_corners, MARKER_SIZE, cam_mat, dist_coef
            )

            # Store the camera frame positions and real-world positions of corner markers
            camera_points = []
            world_points = []

            for i, (ids, corners) in enumerate(zip(marker_IDs, marker_corners)):
                marker_id = ids[0]

                # Process the corner markers (IDs 0, 1, 2, 3)
                if marker_id in marker_coords:
                    camera_points.append([tVec[i][0][0], tVec[i][0][1]])
                    world_points.append(marker_coords[marker_id])

            # Calculate the homography matrix if all 4 corner markers are detected
            if len(camera_points) == 4:
                camera_points = np.array(camera_points, dtype=np.float32)
                world_points = np.array(world_points, dtype=np.float32)
                homography_matrix, _ = cv.findHomography(camera_points, world_points)

            # Process robot and object markers
            for i, (ids, corners) in enumerate(zip(marker_IDs, marker_corners)):
                marker_id = ids[0]

                # Process the robot marker
                if marker_id == ROBOT_MARKER_ID and homography_matrix is not None:
                    robot_position = get_real_world_coordinates(tVec[i], homography_matrix)
                    robot_path.append(robot_position)

                    # Send robot position and path to the web client
                    socketio.emit("update_position", {
                        "robot": {"x": robot_position[0], "y": robot_position[1]},
                        "path": [{"x": p[0], "y": p[1]} for p in robot_path]
                    })

                # Process the object marker
                if marker_id == OBJECT_MARKER_ID and homography_matrix is not None:
                    object_position = get_real_world_coordinates(tVec[i], homography_matrix)

                    # Send object position to the web client
                    socketio.emit("update_position", {
                        "object": {"x": object_position[0], "y": object_position[1]},
                    })

    cap.release()

# Route for serving the webpage
@app.route("/")
def index():
    return render_template("index.html")

# Start the tracking in a background thread
@socketio.on("start_tracking")
def start_tracking():
    tracking_thread = threading.Thread(target=track_robot)
    tracking_thread.daemon = True
    tracking_thread.start()

if __name__ == "__main__":
    socketio.run(app, debug=True)
