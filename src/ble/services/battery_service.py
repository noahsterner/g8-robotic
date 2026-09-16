from ble.characteristics.battery_service.battery_level_characteristic import BatteryLevelCharacteristic
from tcp.tcp_client import TcpClient
from ble.api.service import Service
from ble.api.characteristic import Characteristic

class BatteryService(Service):
    advertise = True

    def __init__(self, tcp_client: TcpClient):
        super().__init__(tcp_client)

    @property
    def characteristics(self) -> list[Characteristic]:
        return [BatteryLevelCharacteristic(self._tcp_client, self.service_id)]

    @property
    def uuid(self) -> str:
        return "180F"

    @property
    def service_id(self) -> int:
        return 2
