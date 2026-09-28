# file: ./src/ble/services/battery_service.py

from ble.characteristics.battery_service.battery_level_characteristic import BatteryLevelCharacteristic
from tcp.tcp_client import TcpClient
from ble.api.service import Service
from ble.api.characteristic import Characteristic

class BatteryService(Service):
    advertise = True

    def __init__(self, battery: Battery):
        super().__init__()
        self._battery: Battery = battery

    @property
    def characteristics(self) -> list[Characteristic]:
        return [
            BatteryLevelCharacteristic(self._battery, self.service_id)
        ]

    @property
    def uuid(self) -> str:
        return "FF10"

    @property
    def service_id(self) -> int:
        return 2
