from ble.characteristics.command_service.command_characteristics import CommandCharactersitics
from ble.characteristics.command_service.setmode_characteristics import SetModeCharacteristics
from tcp.tcp_client import TcpClient
from ble.api.service import Service
from ble.api.characteristic import Characteristic
from core.robot import Robot

class CommandService(Service):
    def __init__(self, robot: Robot):
        super().__init__()
        self._robot: Robot = robot

    @property
    def characteristics(self) -> list[Characteristic]:
        return [
                CommandCharactersitics(self._robot, self.service_id),
                SetModeCharacteristics(self._robot, self.service_id)
        ]

    @property
    def uuid(self) -> str:
        return "FF00"

    @property
    def service_id(self) -> int:
        return 1
