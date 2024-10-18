import cv2 as cv
import numpy as np

# Load the generated markers with corrected file paths
marker_0 = cv.imread(r"C:\Users\viran\Downloads\OpenCV-main\1. generate_markers\markers\marker_0.png", cv.IMREAD_GRAYSCALE)
marker_1 = cv.imread(r"C:\Users\viran\Downloads\OpenCV-main\1. generate_markers\markers\marker_1.png", cv.IMREAD_GRAYSCALE)
marker_2 = cv.imread(r"C:\Users\viran\Downloads\OpenCV-main\1. generate_markers\markers\marker_2.png", cv.IMREAD_GRAYSCALE)
marker_3 = cv.imread(r"C:\Users\viran\Downloads\OpenCV-main\1. generate_markers\markers\marker_3.png", cv.IMREAD_GRAYSCALE)

# Check if all markers are loaded properly
if marker_0 is None or marker_1 is None or marker_2 is None or marker_3 is None:
    print("Error: One or more marker images couldn't be loaded.")
    exit()

# Assuming all markers are the same size
MARKER_SIZE = marker_0.shape[0]

# Create a larger canvas to hold the 4 markers in a square
canvas_size = MARKER_SIZE * 2
canvas = np.zeros((canvas_size, canvas_size), dtype=np.uint8)

# Place the markers on the canvas to form a square
canvas[0:MARKER_SIZE, 0:MARKER_SIZE] = marker_0  # Top-left
canvas[0:MARKER_SIZE, MARKER_SIZE:canvas_size] = marker_1  # Top-right
canvas[MARKER_SIZE:canvas_size, 0:MARKER_SIZE] = marker_2  # Bottom-left
canvas[MARKER_SIZE:canvas_size, MARKER_SIZE:canvas_size] = marker_3  # Bottom-right

# Display the canvas with the arranged markers
cv.imshow("Cartesian Plane with Markers", canvas)

# Optionally save the image
cv.imwrite("C:/Users/viran/Downloads/OpenCV-main/markers/cartesian_plane.png", canvas)

cv.waitKey(0)
cv.destroyAllWindows()
