# import requests

# # ESP32 IP address (replace with your ESP32's actual IP)
# ESP32_IP = "192.168.137.8"  # Default IP for ESP32 in AP mode

# # Coordinates of the robot and the object
# robot_coordinates = {"x": 10.0, "y": 20.0}
# object_coordinates = {"x": 50.0, "y": 30.0}

# # Function to send coordinates to the ESP32
# def send_coordinates_to_esp():
#     try:
#         response = requests.get(
#             f"http://{ESP32_IP}/set_coordinates",
#             params={
#                 "robotX": robot_coordinates["x"],
#                 "robotY": robot_coordinates["y"],
#                 "objectX": object_coordinates["x"],
#                 "objectY": object_coordinates["y"],
#             },
#         )

#         if response.status_code == 200:
#             print("Coordinates sent successfully!")
#         else:
#             print(f"Failed to send coordinates: {response.status_code}, {response.text}")
#     except Exception as e:
#         print(f"Error: {e}")

# # Send the coordinates
# send_coordinates_to_esp()

import requests

# ESP32 Configuration
ESP32_IP = "192.168.137.8"  # Replace with your ESP32's IP address

# Function to send coordinates to ESP32
def send_coordinates_to_esp(robot_position, object_position):
    try:
        # Construct the request URL
        response = requests.get(
            f"http://{ESP32_IP}/set_coordinates",
            params={
                "robotX": robot_position[0],
                "robotY": robot_position[1],
                "objectX": object_position[0],
                "objectY": object_position[1],
            },
            timeout=10,  # Set timeout to 10 seconds
        )
        
        # Check the response status
        if response.status_code == 200:
            print("Coordinates sent successfully!")
        else:
            print(f"Failed to send coordinates: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending coordinates to ESP32: {e}")

# Main function
if __name__ == "__main__":
    # Static test coordinates
    robot_position = (78.213, -34.761)  # Replace with the test robot position
    object_position = (33.177, -33.525)  # Replace with the test object position

    print(f"Testing with Robot Position: {robot_position}, Object Position: {object_position}")
    
    # Send the test coordinates to ESP32
    send_coordinates_to_esp(robot_position, object_position)
