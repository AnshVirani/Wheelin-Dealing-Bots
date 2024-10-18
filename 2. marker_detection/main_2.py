import cv2 as cv
from cv2 import aruco
import numpy as np

# Dictionary to specify type of the marker
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)

# Detector parameters
param_markers = aruco.DetectorParameters()

# Utilize the default camera/webcam driver (adjust the index if needed)
cap = cv.VideoCapture(0)

# Iterate through frames from the live video feed
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the frame to grayscale for ArUco marker detection
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect markers in the grayscale frame
    marker_corners, marker_IDs, _ = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )

    # Only proceed if markers are detected
    if marker_corners:
        # Create a list to store detected marker IDs
        detected_ids = [ids[0] for ids in marker_IDs]

        # Check if all 4 required marker IDs (0, 1, 2, 3) are detected
        if all(x in detected_ids for x in [0, 1, 2, 3]):
            # Loop over all detected markers and draw them
            for ids, corners in zip(marker_IDs, marker_corners):
                if ids[0] in [0, 1, 2, 3]:  # Only process markers 0, 1, 2, 3
                    # Draw the marker's outline
                    cv.polylines(frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA)

                    # Get the top-left corner of the marker for labeling the ID
                    corners = corners.reshape(4, 2).astype(int)
                    top_left = corners[0].ravel()

                    # Draw the marker ID text
                    cv.putText(
                        frame,
                        f"ID: {ids[0]}",
                        tuple(top_left),
                        cv.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (255, 0, 0),  # Blue color for the ID text
                        2,
                        cv.LINE_AA,
                    )
        else:
            # If not all markers are detected, display a message
            cv.putText(frame, "Not all markers detected", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame with the detected markers
    cv.imshow("Marker Detection", frame)

    # Break the loop if 'q' key is pressed
    key = cv.waitKey(1)
    if key == ord("q"):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv.destroyAllWindows()
