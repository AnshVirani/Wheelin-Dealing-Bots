import cv2 as cv
from cv2 import aruco
import numpy as np
import math

# Load in the calibration data
calib_data = np.load(r"C:\Users\viran\Downloads\OpenCV-main\Wheelin-Dealing-Bots\4. calib_data\MultiMatrix.npz")


# Extract the camera calibration matrices
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]

MARKER_SIZE = 6  # Size of the markers in cm (adjust if needed)

# Define the known coordinates of each corner marker
marker_coords = {
    0: (0, 0),      # Marker 0 at (0, 0)
    1: (150, 0),    # Marker 1 at (150, 0)
    2: (150, -60),  # Marker 2 at (150, -60)
    3: (0, -60),    # Marker 3 at (0, -60)
}

# The robot's marker ID
ROBOT_MARKER_ID = 4

# Define the dictionary for ArUco markers
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
param_markers = aruco.DetectorParameters()

# Function to convert rotation vector (rVec) to Euler angles (yaw, pitch, roll)
def rvec_to_euler(rvec):
    R, _ = cv.Rodrigues(rvec)  # Convert rotation vector to a 3x3 rotation matrix
    sy = math.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
    singular = sy < 1e-6  # Check if near zero

    if not singular:
        yaw = math.atan2(R[2, 1], R[2, 2])  # Yaw
        pitch = math.atan2(-R[2, 0], sy)  # Pitch
        roll = math.atan2(R[1, 0], R[0, 0])  # Roll
    else:
        yaw = math.atan2(-R[1, 2], R[1, 1])
        pitch = math.atan2(-R[2, 0], sy)
        roll = 0

    return yaw, pitch, roll

# Start capturing video from the webcam
cap = cv.VideoCapture(0)

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

        # Iterate over the detected markers
        for i, (ids, corners) in enumerate(zip(marker_IDs, marker_corners)):
            marker_id = ids[0]
            # Process corner markers 0, 1, 2, 3
            if marker_id in [0, 1, 2, 3]:
                # Draw the marker's outline on the frame
                cv.polylines(frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA)

                # Extract the marker's corner positions
                corners = corners.reshape(4, 2).astype(int)
                top_left = tuple(corners[0].ravel())

                # Calculate the distance from the camera (Euclidean distance from tVec)
                distance = np.sqrt(tVec[i][0][2]**2 + tVec[i][0][0]**2 + tVec[i][0][1]**2)

                # Draw the coordinate system for the detected marker
                cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)

                # Get the real-world coordinates (from the predefined marker coordinates)
                real_world_x, real_world_y = marker_coords[marker_id]

                # Display the marker ID, distance, and its real-world coordinates
                cv.putText(
                    frame,
                    f"ID: {marker_id}, Dist: {round(distance, 2)}cm",
                    top_left,
                    cv.FONT_HERSHEY_PLAIN,
                    1.5,
                    (0, 0, 255),
                    2,
                    cv.LINE_AA,
                )
                cv.putText(
                    frame,
                    f"World Coords: X:{real_world_x}cm Y:{real_world_y}cm",
                    (top_left[0], top_left[1] + 30),
                    cv.FONT_HERSHEY_PLAIN,
                    1.5,
                    (0, 0, 255),
                    2,
                    cv.LINE_AA,
                )

            # Process the robot's marker (ID 19)
            if marker_id == ROBOT_MARKER_ID:
                # Draw the robot's marker outline
                cv.polylines(frame, [corners.astype(np.int32)], True, (0, 255, 0), 4, cv.LINE_AA)

                # Convert the rotation vector to Euler angles to get the orientation
                yaw, pitch, roll = rvec_to_euler(rVec[i])

                # Extract the marker's corner positions for displaying text
                corners = corners.reshape(4, 2).astype(int)
                top_left = tuple(corners[0].ravel())

                # Display the robot's position and orientation
                cv.putText(
                    frame,
                    f"Robot Marker ID: {marker_id}",
                    top_left,
                    cv.FONT_HERSHEY_PLAIN,
                    1.5,
                    (0, 255, 0),
                    2,
                    cv.LINE_AA,
                )
                cv.putText(
                    frame,
                    f"Yaw (deg): {round(math.degrees(yaw), 2)}",
                    (top_left[0], top_left[1] + 30),
                    cv.FONT_HERSHEY_PLAIN,
                    1.5,
                    (0, 255, 0),
                    2,
                    cv.LINE_AA,
                )
                cv.putText(
                    frame,
                    f"Pos: X: {round(tVec[i][0][0], 2)} Y: {round(tVec[i][0][1], 2)} Z: {round(tVec[i][0][2], 2)}",
                    (top_left[0], top_left[1] + 60),
                    cv.FONT_HERSHEY_PLAIN,
                    1.5,
                    (0, 255, 0),
                    2,
                    cv.LINE_AA,
                )

    # Display the video frame with the marker information
    cv.imshow("Marker and Robot Detection", frame)

    # Break the loop when the 'q' key is pressed
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv.destroyAllWindows()
