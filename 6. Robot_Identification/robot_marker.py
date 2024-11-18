import cv2 as cv
import numpy as np
import random

# Dictionary to generate the ArUco markers
marker_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_5X5_250)

# Define marker size (real world)
MARKER_SIZE_CM = 6  # 6 cm marker size

# Scaling factor: 10 pixels per cm
PIXELS_PER_CM = 10

# Convert marker size to pixels
marker_size_px = int(MARKER_SIZE_CM * PIXELS_PER_CM)

# Generate markers for 0, 1, 2, 3, and 4, each of size based on the real world
marker_0 = cv.aruco.generateImageMarker(marker_dict, 0, marker_size_px)  # Marker 0
marker_1 = cv.aruco.generateImageMarker(marker_dict, 1, marker_size_px)  # Marker 1
marker_2 = cv.aruco.generateImageMarker(marker_dict, 2, marker_size_px)  # Marker 2
marker_3 = cv.aruco.generateImageMarker(marker_dict, 3, marker_size_px)  # Marker 3
marker_19 = cv.aruco.generateImageMarker(marker_dict, 4, marker_size_px)  # Marker 19 (for the robot)

# Create a blank canvas with a grey background, scaled to 150 cm x 60 cm (in pixels)
canvas_width = int(150 * PIXELS_PER_CM)
canvas_height = int(60 * PIXELS_PER_CM)
canvas = np.ones((canvas_height, canvas_width), dtype=np.uint8) * 128  # Grey background

# Place the four corner markers based on the real-world coordinates
# Top-left: Marker 0 at (0, 0)
canvas[0:marker_size_px, 0:marker_size_px] = marker_0

# Top-right: Marker 1 at (150 cm, 0 cm)
canvas[0:marker_size_px, -marker_size_px:] = marker_1

# Bottom-left: Marker 2 at (0 cm, -60 cm)
canvas[-marker_size_px:, 0:marker_size_px] = marker_2

# Bottom-right: Marker 3 at (150 cm, -60 cm)
canvas[-marker_size_px:, -marker_size_px:] = marker_3

# Randomly place marker 19 at a random location and with a random rotation
# Randomly choose x and y coordinates inside the canvas, avoiding the corners
x_rand = random.randint(marker_size_px, canvas_width - marker_size_px)
y_rand = random.randint(marker_size_px, canvas_height - marker_size_px)
angle_rand = random.randint(0, 360)  # Random angle for rotation

# Rotate marker 19 by a random angle
rotation_matrix = cv.getRotationMatrix2D((marker_size_px // 2, marker_size_px // 2), angle_rand, 1.0)
rotated_marker_19 = cv.warpAffine(marker_19, rotation_matrix, (marker_size_px, marker_size_px))

# Place marker 19 on the canvas at a random position
canvas[y_rand:y_rand + marker_size_px, x_rand:x_rand + marker_size_px] = rotated_marker_19

# Save and display the final canvas with markers
cv.imshow("Marker Placement", canvas)
cv.imwrite("marker_layout_150cmx60cm.png", canvas)
cv.waitKey(0)
cv.destroyAllWindows()
