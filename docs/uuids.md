# GATT Services
The robot exposes the following GATT services:


| Service | Description |
|---|---|
| [Control](#Control) | Control for the robot |
| [Battery](#Battery) | Provides battery information |

## Control
This service is used to control the robots movement. It provides characteristics for the desired speed and steering angle data

### Service UUID 
0000FF00-0000-1000-8000-00805F9B34FB 

### Characteristics 

#### Drive command 
Controls the speed and steering of the robot. 

- UUID: 0000FF01-0000-1000-8000-00805F9B34FB 
- Flags: Write 
- Data: 4 bytes 


| Byte | Field | Type |
|---|---|---|
| 0:2 | tspeed | uint16 |
| 2:4 | tangle | uint16 |

#### Set robot mode
Sets the mode of the robot. 

- UUID: 0000FF02-0000-1000-8000-00805F9B34FB 
- Flags: Write, Read, Notify
- Data: 1 bytes 


| Byte | Field | Type |
|---|---|---|
| 0:1 | mode | uint8 |

| Byte | Mode |
|---|---|
| 0x00 (0) | Manual | 
| 0x01 (1) | Auto |

## Battery
This service is used to provide information to the central about the robots battery level.

### Service UUID 
0000FF10-0000-1000-8000-00805F9B34FB 

### Characteristics 

#### Battery Level 
Provides the robots battery level as a percentage within the range (0-100).

- UUID: 0000FF11-0000-1000-8000-00805F9B34FB
- Flags: Read, Notify 
- Data: 1 bytes 


| Byte | Field | Type |
|---|---|---|
| 0 | tIBattery_Level | uint8 |
