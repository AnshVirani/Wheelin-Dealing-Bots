import cv2 as cv
from cv2 import aruco
import numpy as np

# Dictionary to specify type of the ArUco marker
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)

# Create parameters for marker detection and adjust some settings
param_markers = aruco.DetectorParameters()

# Dictionary to specify type of the ArUco marker
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)

# Create parameters for marker detection and adjust some settings
param_markers = aruco.DetectorParameters()

# Optional: Adjust parameters to improve detection
param_markers.cornerRefinementMethod = aruco.CORNER_REFINE_CONTOUR  # Refine detection
param_markers.adaptiveThreshConstant = 7  # Adjust thresholding for better marker detection

# Utilize the default camera/webcam driver
cap = cv.VideoCapture(0)

# Iterate through frames from the live video feed
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the frame to grayscale for ArUco marker detection
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect markers in the grayscale frame
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )

    # Proceed only if at least some markers are detected
    if marker_corners and len(marker_IDs) >= 4:
        detected_ids = [ids[0] for ids in marker_IDs]
        # Check if all required marker IDs (0, 1, 2, 3) are detected
        if all(x in detected_ids for x in [0, 1, 2, 3]):
            for ids, corners in zip(marker_IDs, marker_corners):
                if ids[0] in [0, 1, 2, 3]:  # Only consider markers 0, 1, 2, 3
                    # Draw the outline of the marker (polylines around the marker)
                    cv.polylines(
                        frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
                    )
                    
                    # Draw a rectangle bounding box around the marker
                    corners = corners.reshape(4, 2).astype(int)
                    top_left = tuple(corners[0])
                    bottom_right = tuple(corners[2])
                    cv.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

                    # Get the position of the top-left corner for displaying the ID
                    top_right = tuple(corners[0])

                    # Display the marker ID on the frame near the top-left corner
                    cv.putText(
                        frame,
                        f"ID: {ids[0]}",
                        top_right,
                        cv.FONT_HERSHEY_PLAIN,
                        1.3,
                        (200, 100, 0),
                        2,
                        cv.LINE_AA,
                    )

    # Display the frame with the detected markers and bounding boxes
    cv.imshow("Marker Detection", frame)

    # Break the loop if 'q' key is pressed
    key = cv.waitKey(1)
    if key == ord("q"):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv.destroyAllWindows()

param_markers.cornerRefinementMethod = aruco.CORNER_REFINE_CONTOUR  # Use contour refinement to enhance detection
param_markers.adaptiveThreshConstant = 7  # Adjust thresholding for better marker detection
param_markers.minMarkerPerimeterRate = 0.03  # Ensure smaller markers are detected

# Utilize the default camera/webcam driver
cap = cv.VideoCapture(0)

# Iterate through frames from the live video feed
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the frame to grayscale for ArUco marker detection
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect markers in the grayscale frame
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )

    # Only proceed if markers are detected
    if marker_corners:
        for ids, corners in zip(marker_IDs, marker_corners):
            # Draw the outline of the marker
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            # Convert corners to integer coordinates
            corners = corners.reshape(4, 2).astype(int)
            
            # Get the position of the top-right corner for displaying the ID
            top_right = corners[0].ravel()

            # Display the marker ID on the frame near the top-right corner
            cv.putText(
                frame,
                f"ID: {ids[0]}",
                tuple(top_right),
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (200, 100, 0),
                2,
                cv.LINE_AA,
            )

    # Display the frame with the detected markers
    cv.imshow("Marker Detection", frame)

    # Break the loop if 'q' key is pressed
    key = cv.waitKey(1)
    if key == ord("q"):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv.destroyAllWindows()
