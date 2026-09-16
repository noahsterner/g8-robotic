# file: ./src/ble/api/characteristic.py
import logging
from typing import Any

from bluezero.peripheral import Peripheral
from ble.api.flags import CharacteristicFlags
from tcp.tcp_client import TcpClient

logger = logging.getLogger(__name__)

class Characteristic:
    """Base class for a GATT characteristic.

    A characteristics belongs to a service and defines the behaviour for reading, writing and notifications.
    """

    characteristic_id: int
    uuid: str
    flags: list[CharacteristicFlags]
    value: list[Any]
    notifying: bool

    def __init__(self, tcp_client: TcpClient, service_id) -> None:
        self._tcp_client: TcpClient = tcp_client
        self.service_id: int = service_id

    def write_value(self, value, options):
        """Updates the characteristic value."""
        return None

    def read_value(self) -> list[int] | None:
        """Reads the value of the characteristic

        Return the characteristic value as a list of uint8 values.
        """
        return None

    def notify(self, notifying: bool, characteristic) -> None:
        """Toggle notifications."""
        return None


    def setup(self, peripheral: Peripheral) -> None:
        peripheral.add_characteristic(
                srv_id = self.service_id,
                chr_id = self.characteristic_id,
                uuid = self.uuid,
                value = self.value,
                flags = self.flags,
                notifying = self.notifying,
                read_callback = self.read_value,
                write_callback = self.write_value,
                notify_callback = self.notify,
        )

        logger.info("registered characteristic: %s", self.uuid)

