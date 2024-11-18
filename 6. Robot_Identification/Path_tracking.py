import cv2 as cv
from cv2 import aruco
import numpy as np
import math

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

# Function to convert rotation vector (rVec) to yaw angle in degrees
def get_yaw_angle(rVec):
    R, _ = cv.Rodrigues(rVec)  # Convert rotation vector to a rotation matrix
    yaw = math.atan2(R[1, 0], R[0, 0])  # Calculate yaw (rotation around Z-axis)
    return math.degrees(yaw)  # Convert radians to degrees

# Visualization window parameters
visualization_width = 300  # Width of the visualization window
visualization_height = 120  # Height of the visualization window
scale = 2  # Scale factor for converting real-world cm to pixels

# Initialize visualization canvas
visualization_canvas = np.ones((visualization_height, visualization_width, 3), dtype=np.uint8) * 255  # White background

# Function to draw the robot's path on the visualization canvas
def draw_path(canvas, path, color=(0, 0, 255), label="Robot"):
    for i in range(1, len(path)):
        x1, y1 = int(path[i-1][0] / scale), int(-path[i-1][1] / scale)
        x2, y2 = int(path[i][0] / scale), int(-path[i][1] / scale)
        cv.line(canvas, (x1, y1), (x2, y2), color, 2)
    # Add label to the latest position
    if path:
        x_last, y_last = int(path[-1][0] / scale), int(-path[-1][1] / scale)
        cv.putText(
            canvas,
            label,
            (x_last + 5, y_last - 5),  # Offset for readability
            cv.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            1,
            cv.LINE_AA,
        )

# Start capturing video from the webcam
cap = cv.VideoCapture(0)

# Initialize variables
robot_path = []
homography_matrix = None  # Homography matrix to map camera frame to world frame

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale for marker detection
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect markers in the grayscale frame
    marker_corners, marker_IDs, _ = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )

    # If markers are detected
    if marker_corners:
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
                # Add the marker's camera frame position (tVec) and real-world position
                camera_points.append([tVec[i][0][0], tVec[i][0][1]])
                world_points.append(marker_coords[marker_id])

                # Highlight and display real-world coordinates for corner markers
                corners = corners.reshape(4, 2).astype(int)
                cv.polylines(frame, [corners], True, (255, 255, 0), 3, cv.LINE_AA)  # Yellow bounding box
                top_left = tuple(corners[0].ravel())
                real_world_x, real_world_y = marker_coords[marker_id]
                cv.putText(
                    frame,
                    f"Corner {marker_id}: ({real_world_x}cm, {real_world_y}cm)",
                    (top_left[0], top_left[1] - 10),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 0),
                    2,
                    cv.LINE_AA,
                )

        # Calculate the homography matrix if all 4 corner markers are detected
        if len(camera_points) == 4:
            camera_points = np.array(camera_points, dtype=np.float32)
            world_points = np.array(world_points, dtype=np.float32)
            homography_matrix, _ = cv.findHomography(camera_points, world_points)

        # Process robot markers using the homography matrix
        robot_position = None

        for i, (ids, corners) in enumerate(zip(marker_IDs, marker_corners)):
            marker_id = ids[0]

            # Process the robot marker
            if marker_id == ROBOT_MARKER_ID and homography_matrix is not None:
                robot_position = get_real_world_coordinates(tVec[i], homography_matrix)
                robot_path.append(robot_position)

                # Display robot position
                corners = corners.reshape(4, 2).astype(int)
                top_left = tuple(corners[0].ravel())
                cv.putText(frame, f"Robot: X:{robot_position[0]:.1f} Y:{robot_position[1]:.1f}", (top_left[0], top_left[1] + 30), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2, cv.LINE_AA)

        # Draw the robot's path on the visualization canvas
        visualization_canvas.fill(255)  # Clear the canvas (white background)
        draw_path(visualization_canvas, robot_path)

    # Display the video frame with the marker information
    cv.imshow("Robot and Object Tracking", frame)

    # Display the path visualization
    cv.imshow("Robot Path Visualization", visualization_canvas)

    # Break the loop when the 'q' key is pressed
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv.destroyAllWindows()
