import cv2 as cv
from cv2 import aruco
import numpy as np

# Load the ArUco dictionary
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)

# Initialize detector parameters manually
param_markers = aruco.DetectorParameters()

# Utilize the default camera/webcam driver
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect markers
    marker_corners, marker_IDs, _ = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )

    if marker_corners:
        detected_ids = [ids[0] for ids in marker_IDs]

        # Check if required markers are detected
        if all(x in detected_ids for x in [0, 1, 2, 3]):
            for ids, corners in zip(marker_IDs, marker_corners):
                if ids[0] in [0, 1, 2, 3]:
                    cv.polylines(frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA)

                    corners = corners.reshape(4, 2).astype(int)
                    top_left = corners[0].ravel()

                    cv.putText(
                        frame,
                        f"ID: {ids[0]}",
                        tuple(top_left),
                        cv.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (255, 0, 0),
                        2,
                        cv.LINE_AA,
                    )
        else:
            cv.putText(frame, "Not all markers detected", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv.imshow("Marker Detection", frame)

    # Break the loop if 'q' is pressed
    key = cv.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
