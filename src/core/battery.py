# file: ./src/core/battery.py

from core.bridge_protocol import BridgeProtocol
from tcp.tcp_client import TcpClient

class Battery:
    def __init__(self, tcp_client: TcpClient):
        self._tcp_client = tcp_client

    def get_battery_level(self) -> int:
        return int(self._tcp_client.request(BridgeProtocol.get_battery_level())[0])
