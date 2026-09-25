import time
from core.robot import Robot

FRONT_DISTANCE = 0 #change this with the information from lidar 
LEFT_DISTANCE = 0 #unsure if this should be global variable
RIGHT_DISTANCE = 0

class AutoDrive:

    def __init__(self, robot: Robot):
        self.robot = robot

    def drive_automatically(self):
        if FRONT_DISTANCE > 500: #change the 500 to what metric the lidar returns
            self.robot.drive(2000, 0)

        elif RIGHT_DISTANCE > LEFT_DISTANCE:
            self.robot.drive(2000, 2000)
            time.sleep(1) #change sleep and speed to what makes it turns 90 degrees
            self.robot.drive(2000, 0)

        else:
            self.robot.drive(2000, -2000)
            time.sleep(1) #change sleep and speed to what makes it turn 90 degrees
            self.robot.drive(2000, 0)