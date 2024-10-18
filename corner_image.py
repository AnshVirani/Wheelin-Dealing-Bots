import cv2 as cv
import numpy as np

# Load the previously generated markers (0, 1, 2, 3)
marker_0 = cv.imread(r"C:\Users\viran\Downloads\OpenCV-main\1. generate_markers\markers\marker_0.png", cv.IMREAD_GRAYSCALE)
marker_1 = cv.imread(r"C:\Users\viran\Downloads\OpenCV-main\1. generate_markers\markers\marker_1.png", cv.IMREAD_GRAYSCALE)
marker_2 = cv.imread(r"C:\Users\viran\Downloads\OpenCV-main\1. generate_markers\markers\marker_2.png", cv.IMREAD_GRAYSCALE)
marker_3 = cv.imread(r"C:\Users\viran\Downloads\OpenCV-main\1. generate_markers\markers\marker_3.png", cv.IMREAD_GRAYSCALE)

# Check if all markers are loaded properly
if marker_0 is None or marker_1 is None or marker_2 is None or marker_3 is None:
    print("Error: One or more marker images couldn't be loaded.")
    exit()

# Assuming all markers are of the same size (MARKER_SIZE x MARKER_SIZE)
MARKER_SIZE = marker_0.shape[0]

# Define padding between markers (e.g., 50 pixels)
PADDING = 50

# Calculate the canvas size with enough space between markers (padding)
canvas_size = (MARKER_SIZE * 2) + (PADDING * 3)

# Create a blank canvas with a grey background (pixel value 128 for grey)
canvas = np.ones((canvas_size, canvas_size), dtype=np.uint8) * 128  # Grey background

# Place the markers in the 4 corners with padding between them
# Top-left corner
canvas[PADDING:PADDING+MARKER_SIZE, PADDING:PADDING+MARKER_SIZE] = marker_0

# Top-right corner
canvas[PADDING:PADDING+MARKER_SIZE, PADDING*2+MARKER_SIZE:PADDING*2+MARKER_SIZE*2] = marker_1

# Bottom-left corner
canvas[PADDING*2+MARKER_SIZE:PADDING*2+MARKER_SIZE*2, PADDING:PADDING+MARKER_SIZE] = marker_2

# Bottom-right corner
canvas[PADDING*2+MARKER_SIZE:PADDING*2+MARKER_SIZE*2, PADDING*2+MARKER_SIZE:PADDING*2+MARKER_SIZE*2] = marker_3

# Display the canvas with the 4 markers placed at proper distances
cv.imshow("4 Corner Markers", canvas)

# Optionally save the canvas
cv.imwrite(r"C:\path_to_save_output\corner_markers.png", canvas)

cv.waitKey(0)
cv.destroyAllWindows()
