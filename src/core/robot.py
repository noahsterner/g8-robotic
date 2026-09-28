# file: ./src/core/robot.py

from core.bridge_protocol import BridgeProtocol
from core.mode import Mode
from tcp.tcp_client import TcpClient

class RobotState:
    def __init__(self):
        self.mode: Mode = Mode.MANUAL
        self.speed: int = 0
        self.steering: int = 0

class Robot:
    def __init__(self, tcp_client: TcpClient):
        self._tcp_client = tcp_client
        self._state: RobotState = RobotState()
    
    def set_mode(self, mode: Mode) -> None:
        self._mode = mode

    def drive(self, speed: int, steering: int) -> None:
        self._state.speed = speed
        self._state.steering = sterring

        self._tcp_client.request(BridgeProtocol.drive(speed, steering))
