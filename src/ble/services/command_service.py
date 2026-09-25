from ble.characteristics.command_service.command_characteristics import CommandCharactersitics
from ble.characteristics.command_service.automode_characteristics import AutoModeCharacteristic
from tcp.tcp_client import TcpClient
from ble.api.service import Service
from ble.api.characteristic import Characteristic

class CommandService(Service):
    def __init__(self, tcp_client: TcpClient):
        super().__init__(tcp_client)

    @property
    def characteristics(self) -> list[Characteristic]:
        return [
            CommandCharactersitics(self._tcp_client, self.service_id),
            AutoModeCharacteristic(self._tcp_client, self.service_id, self._auto_drive),
                ]

    @property
    def uuid(self) -> str:
        return "FF00"

    @property
    def service_id(self) -> int:
        return 1
