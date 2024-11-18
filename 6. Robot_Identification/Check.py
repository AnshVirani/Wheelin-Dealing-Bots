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

# Visualization parameters
real_width_cm = 150  # Real-world width in cm
real_height_cm = 60  # Real-world height in cm
pixels_per_cm = 5    # Scale factor: 5 pixels per cm
visualization_width = int(real_width_cm * pixels_per_cm)  # Width in pixels
visualization_height = int(real_height_cm * pixels_per_cm)  # Height in pixels

# Initialize visualization canvas
visualization_canvas = np.ones((visualization_height, visualization_width, 3), dtype=np.uint8) * 255  # White background

# Function to draw the real-world canvas
def draw_canvas(canvas, corner_coords):
    for marker_id, coord in corner_coords.items():
        x, y = int(coord[0] * pixels_per_cm), int(coord[1] * pixels_per_cm)
        cv.circle(canvas, (x, y), 10, (0, 0, 255), -1)  # Red circles for corner markers
        cv.putText(canvas, f"Corner {marker_id}", (x + 10, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

# Start capturing video from the webcam
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to access camera feed.")
        break

    # Convert the frame to grayscale for marker detection
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect markers in the grayscale frame
    marker_corners, marker_IDs, _ = aruco.detectMarkers(gray_frame, marker_dict)

    # Debug: Print detected marker IDs
    if marker_IDs is not None:
        print(f"Detected Markers: {marker_IDs.ravel()}")
    else:
        print("No markers detected.")

    # If markers are detected
    if marker_corners:
        # Draw detected markers for visual feedback
        aruco.drawDetectedMarkers(frame, marker_corners, marker_IDs)

    # Display the video frame
    cv.imshow("Marker Detection", frame)

    # Break the loop when the 'q' key is pressed
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv.destroyAllWindows()
