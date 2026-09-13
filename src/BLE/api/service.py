from abc import ABC, abstractmethod

from bluezero.peripheral import Peripheral
from BLE.api.characteristic import Characteristic

class Service(ABC):
    """Base class for a GATT service.

    A service owns its own charactersitics and are responsible for registering them
    """

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
                primary=True
        )

        for characteristic in self.characteristics:
            characteristic.setup(peripheral)


