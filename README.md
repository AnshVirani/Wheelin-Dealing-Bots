# Wheelin-Dealing-Bots
This project showcases the development of a real-time control and coordination system, , multi-robot coordination, and collision avoidance, making it ideal for advanced IoT transportation solutions using multiple omni-wheel robots based on ROS 2 and ArUco marker detection.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Hardware and Software Components](#hardware-and-software-components)
3. [System Architecture](#system-architecture)
4. [Installation and Setup](#installation-and-setup)
5. [Usage](#usage)
6. [Testing](#testing)
7. [Results](#results)
8. [Challenges and Solutions](#challenges-and-solutions)
9. [Future Work](#future-work)
10. [Contributing](#contributing)
11. [License](#license)

---

## Project Overview
This project focuses on developing a real-time multi-robot control and coordination system using ROS 2 and Aruco marker detection. The system enables omni-wheel robots to navigate and avoid collisions in real-time using computer vision techniques and communication with a central controller.

### Key Objectives:
- **Aruco Marker Detection** for real-time position tracking.
- **Multi-Robot Coordination** using ROS 2.
- **Collision Avoidance Algorithms** to ensure safe navigation.
- **Real-Time Communication** between robots and a central controller.

## Hardware and Software Components
### Hardware:
- **ESP32 Microcontrollers** (for controlling individual robots)
- **Omniwheel Robots** (for multidirectional movement)
- **Raspberry Pi 5** (as the central controller)
- **Logitech C270 HD Webcam** (for Aruco marker detection)
- **Servo Motors** (for precise control of robot movements)

### Software:
- **ROS 2** (Robot Operating System)
- **OpenCV** (for Aruco marker detection)
- **Micro-ROS** (for ESP32 communication)
- **Python/C++** (for algorithm development)
- **Wi-Fi** (for communication between Raspberry Pi and ESP32)

## System Architecture
- **Camera Setup and Aruco Detection**: A camera captures the environment and detects Aruco markers attached to each robot.
- **Robot Hardware Control**: ESP32 microcontrollers control motors and communicate movement commands.
- **Central Controller**: A Raspberry Pi running ROS 2 processes vision data and coordinates robot movements.
- **Collision Avoidance**: Real-time algorithms prevent robots from colliding while navigating shared space.

### Diagram (Optional):
_Include a diagram of the system architecture._

## Installation and Setup
### Prerequisites:
- **ROS 2** installed on Raspberry Pi 5
- **OpenCV** for Python or C++
- **ESP32 toolchain** for microcontroller programming

### Step-by-Step Guide:
1. **Camera Calibration**: Use OpenCV to calibrate the camera for accurate detection.
2. **Install ROS 2** on Raspberry Pi.
3. **Set up micro-ROS** on ESP32 for communication.
4. **Install dependencies** (OpenCV, required ROS 2 packages).

_Include any specific commands and configurations needed._

## Usage
1. Power on the Raspberry Pi and ESP32 microcontrollers.
2. Start the ROS 2 nodes on the Raspberry Pi for Aruco detection and robot control.
3. Monitor real-time robot positions and send commands through ROS 2 topics.

_Provide examples of how to run the system, including specific commands._

## Testing
### Test Procedures:
- **Individual Component Testing**: Validate camera calibration, motor control, and communication independently.
- **Integration Testing**: Combine all components and test in a real-world environment.

_Include instructions for running tests and evaluating the system's performance._

## Results
- **Accurate position tracking** with Aruco markers.
- **Smooth robot navigation** and successful collision avoidance.
- **Reliable real-time communication** between all components.

_Include images or videos demonstrating the results._

## Challenges and Solutions
- **Hardware Synchronization Issues**: Resolved by optimizing ROS 2 Quality of Service (QoS) settings.
- **Camera Calibration**: Improved detection accuracy through OpenCV tuning.
- **Collision Avoidance Tuning**: Iterative testing led to improved safety and efficiency.

## Future Work
- Enhance vision algorithms with machine learning.
- Scale the system to manage more robots.
- Integrate additional sensors (e.g., LiDAR) for better environmental perception.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for discussion.

## License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
