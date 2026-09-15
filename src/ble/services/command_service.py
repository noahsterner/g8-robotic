from ble.characteristics.command_service.command_characteristics import CommandCharactersitics
from tcp.tcp_client import TcpClient
from ble.api.service import Service
from ble.api.characteristic import Characteristic

class CommandService(Service):
    def __init__(self, tcp_client: TcpClient):
        super().__init__(tcp_client)

    @property
    def characteristics(self) -> list[Characteristic]:
        return [CommandCharactersitics(self._tcp_client)]

    @property
    def uuid(self) -> str:
        return "f1204501-027a-4d8d-8704-8cb352456dc7"

    @property
    def service_id(self) -> int:
        return 1
