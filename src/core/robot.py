# file: ./src/core/robot.py

from core.bridge_protocol import BridgeProtocol
from tcp.tcp_client import TcpClient

class Robot:
    def __init__(self, tcp_client: TcpClient):
        self._tcp_client = tcp_client

    def drive(self, speed: int, steering: int) -> None:
        self._tcp_client.request(BridgeProtocol.drive(speed, steering))
