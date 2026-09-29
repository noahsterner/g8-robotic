# file: ./src/ble/characteristics/battery_service/battery_level_characteristic.py

import logging
from bluezero import async_tools
from ble.api.characteristic import Characteristic
from ble.api.flags import CharacteristicFlags
from core.robot import Robot

logger = logging.getLogger(__name__)

class BatteryLevelCharacteristic(Characteristic):
    characteristic_id = 1
    uuid = "FF11"
    flags = [CharacteristicFlags.READ, CharacteristicFlags.NOTIFY]
    value = [100]
    notifying = False

    def __init__(self, robot: Robot, service_id: int) -> None:
        super().__init__(service_id)
        self._robot: Robot = robot

    def read_value(self) -> list[int]:
        self.value[0] = self._robot.get_battery_level()
        logger.info("read battery level: %s", self.value)

        return self.value

    def notify(self, notifying: bool, characteristic) -> None:
        self.notifying = notifying

        if(self.notifying):
            async_tools.add_timer_seconds(10, self._pool_battery_level, characteristic)

    def _pool_battery_level(self, characteristic) -> bool:
        new_value: list[int] = self.read_value()
        characteristic.set_value(new_value)

        return self.notifying


