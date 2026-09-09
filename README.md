# Robot Firmware (Raspberry Pi)
The Raspberry Pi codebase that controls the robot’s movement, sensors, camera, and communication with both the mobile app and backend.

## Features
- Autonomous driving logic
- Obstacle detection + avoidance
- Camera capture during avoidance events
- Position reporting to the backend
- Execution of drive commands received from the app
- Queued sending of data when connectivity is unstable

## Requirements Covered
- Autonomous operation (#M1.1)
- Collision avoidance (#M1.2)
- Drive command execution (#M1.3)
- Camera capture + upload (#M1.4)
- Integrates with backend position + image APIs

## Project Info
- Runs on Raspberry Pi with connected sensors and camera
- Communicates with the app via BLE
- Communicates with the backend via REST
- Designed to support both manual and autonomous robot operation

TESTEDIT COMMIT LINE - IGNORE LAST LINE, REMOVE YOUR EYES! :)
