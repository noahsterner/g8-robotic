from ble.characteristics.battery_service.battery_level_characteristics import BatteryLevelCharacteristics
from tcp.tcp_client import TcpClient
from ble.api.service import Service
from ble.api.characteristic import Characteristic

class BatteryService(Service):
    def __init__(self, tcp_client: TcpClient):
        super().__init__(tcp_client)

    @property
    def characteristics(self) -> list[Characteristic]:
        return [BatteryLevelCharacteristics(self._tcp_client)]

    @property
    def uuid(self) -> str:
        return "0000180F-0000-1000-8000-00805F9B34FB"

    @property
    def service_id(self) -> int:
        return 2
