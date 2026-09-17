import logging

from ble.api.characteristic import Characteristic
from ble.api.flags import CharacteristicFlags
from tcp.tcp_client import TcpClient

logger = logging.getLogger(__name__)

class BatteryLevelCharacteristic(Characteristic):
    characteristic_id = 1
    uuid = "FF11"
    flags = [CharacteristicFlags.READ]
    value = [100]
    notifying = False

    def __init__(self, tcp_client: TcpClient, service_id: int) -> None:
        super().__init__(tcp_client, service_id)

    def read_value(self) -> list[int]:
        self.value[0] -= 1
        logger.info("read battery level: %s", self.value)
        return self.value
