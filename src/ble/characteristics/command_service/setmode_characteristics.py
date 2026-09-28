# file: ./src/ble/characteristics/command_service/setmode_characteristics.py

import logging

from bluezero import async_tools
from ble.api.characteristic import Characteristic
from ble.api.flags import CharacteristicFlags
from core.robot import Robot
from core.mode import Mode

logger = logging.getLogger(__name__)

class SetModeCharacteristics(Characteristic):
    characteristic_id = 2
    uuid = "FF02"
    flags = [
            CharacteristicFlags.WRITE,
            CharacteristicFlags.READ,
            CharacteristicFlags.NOTIFY,
    ]
    value = [0]
    notifying = False; 

    def __init__(self, robot: Robot, service_id: int) -> None:
        super().__init__(service_id)
        self._robot = robot

    def write_value(self, value: list[int], options):
        self.value = value; 
        mode: Mode = Mode(value[0])

        logger.info("set robot mode: %s", mode)
        self._robot.set_mode(mode)

    def read_value(self) -> list[int]:
        logger.info("read robot mode: %s", Mode(self.value[0]))
        return self.value

    def notify(self, notifying: bool, characteristic) -> None:
        self.notifying = notifying

        if(self.notifying):
            async_tools.add_timer_seconds(10, self._pool_mode, characteristic)

    def _pool_mode(self, characteristic) -> bool:
        new_value: list[int] = self.read_value()
        characteristic.set_value(new_value)

        return self.notifying

