import logging

from ble.api.characteristic import Characteristic
from ble.api.flags import CharacteristicFlags
from tcp.tcp_client import TcpClient
from autoDrive.autodrive import AutoDrive

logger = logging.getLogger(__name__)

class AutoModeCharacteristic(Characteristic):
    characteristic_id = 2
    uuid = "FF02"
    flags = [CharacteristicFlags.WRITE]
    value = [0]
    notifying = False; 

    def __init__(self, tcp_client: TcpClient, service_id: int, auto_drive: AutoDrive) -> None:
        super().__init__(tcp_client, service_id)
        self._auto_drive = auto_drive

    def write_value(self, value, options):
        self.value = value; 
        enabled = bool(value[0])

        logger.info("write automode command (enabled: %s)", enabled)

        if enabled:
            self._auto_drive.start_automove
        else:
            self._auto_drive.stop_automove
