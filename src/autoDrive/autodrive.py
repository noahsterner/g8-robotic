import time
import logging
import threading
from core.robot import Robot

logger = logging.getLogger(__name__)

FRONT_DISTANCE = 0 #change this with the information from lidar 
LEFT_DISTANCE = 0 #unsure if this should be global variable
RIGHT_DISTANCE = 0

class AutoDrive:
    def __init__(self, robot: Robot):
        self.robot = robot
        self._running = threading.Event()
        self._thread = None

    def start_automove(self):
        if self._thread and self._thread.is_alive():
            logger.info("Autodrive is already active")
            return
        logger.info("starting autodrive")
        self._running.set()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop_automove(self):
        logger.info("Stopping autodrive")
        self._running.clear()
        self.robot.drive(0, 0)

    def _loop(self):
        while self._running.is_set():
            self.drive_automatically()
            time.sleep(0.1)

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