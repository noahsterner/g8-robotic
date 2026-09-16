from tcp.tcp_client import TcpClient
from ble.api.service import Service
from ble.api.characteristic import Characteristic

class BatteryService(Service):
    advertise = False

    def __init__(self, tcp_client: TcpClient):
        super().__init__(tcp_client)

    @property
    def characteristics(self) -> list[Characteristic]:
        return []

    @property
    def uuid(self) -> str:
        return "15C201EF-A228-4ADF-A1A1-41D1801EB0E2"

    @property
    def service_id(self) -> int:
        return 2
