import logging

from ble.api.characteristic import Characteristic
from ble.api.flags import CharacteristicFlags
from tcp.tcp_client import TcpClient

logger = logging.getLogger(__name__)

class CommandCharactersitics(Characteristic):
    characteristic_id = 1
    uuid = "FF01"
    flags = [CharacteristicFlags.WRITE]
    value = [0,0,0,0]
    notifying = False

    def __init__(self, tcp_client: TcpClient, service_id: int) -> None:
        super().__init__(tcp_client, service_id)

    def write_value(self, value, options):
        """Updates the characteristic value."""

        self.value = value

        speed: int = int.from_bytes(bytes(self.value[0:2]), byteorder="big", signed=True)
        steering: int = int.from_bytes(bytes(self.value[2:4]), byteorder="big", signed=True)

        logger.info("write drive command (speed: %d, steering: %d)", speed, steering)
        self._tcp_client.request(f"Driver.Drive(speed:{speed}, steering:{steering})")

