# file: ./src/ble/characteristics/command_service/setmode_characteristics.py

import logging

from ble.api.characteristic import Characteristic
from ble.api.flags import CharacteristicFlags
from core.robot import Robot
from core.mode import Mode

logger = logging.getLogger(__name__)

class SetModeCharacteristics(Characteristic):
    characteristic_id = 2
    uuid = "FF02"
    flags = [CharacteristicFlags.WRITE]
    value = [0]
    notifying = False; 

    def __init__(self, robot: Robot, service_id: int) -> None:
        super().__init__(service_id)
        self._robot = robot

    def write_value(self, value, options):
        self.value = value; 
        mode = Mode(value[0])

        logger.info("set robot mode (mode: %s)", mode)
        self._robot.set_mode(mode)

