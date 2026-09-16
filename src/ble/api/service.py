# file: ./src/ble/api/service.py
import logging
from abc import ABC, abstractmethod

from bluezero.peripheral import Peripheral
from ble.api.characteristic import Characteristic
from tcp.tcp_client import TcpClient

logger = logging.getLogger(__name__)

class Service(ABC):
    """Base class for a GATT service.

    A service owns its own charactersitics and are responsible for registering them
    """
    
    advertise: bool = True

    def __init__(self, tcp_client: TcpClient):
        self._tcp_client = tcp_client

    @property
    @abstractmethod
    def characteristics(self) -> list[Characteristic]:
        return []

    @property
    @abstractmethod
    def uuid(self) -> str:
        pass

    @property
    @abstractmethod
    def service_id(self) -> int:
        pass

    def setup(self, peripheral: Peripheral) -> None:
        """Add this server to given peripheral"""

        peripheral.add_service(
                srv_id=self.service_id, 
                uuid=self.uuid,
                primary=self.advertise
        )

        logger.info("registered service: %s", self.uuid)

        for characteristic in self.characteristics:
            characteristic.setup(peripheral)


