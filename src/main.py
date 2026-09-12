from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable

from bluezero import async_tools
from bluezero.peripheral import Peripheral
from bluezero import adapter

@dataclass
class charactersitic:
    """Base class for a GATT characteristic.

    A charactersitics belongs to a service and defines the behaviour for reading, writing and notifications.
    """
    srv_id: int
    chr_id: int
    uuid: str
    flags: list[str]
    value: list[Any]
    notifying: bool

    def read_value(self) -> list[int]:
        """Reads the value of the characteristic

        Return the characteristic value as a list of uint8 values.
        """
        raise NotImplementedError

    def update_value(self, charactersitics: charactersitic) -> bool:
        """Updates the characteristic value."""
        raise NotImplementedError

    def notify(self, notifying: bool, charactersitic: charactersitic) -> None:
        """Toggle notifications."""
        raise NotImplementedError

class service(ABC)  :
    """Base class for a GATT service.

    A service owns its own charactersitics and are responsible for registering them
    """

    uuid: str
    srv_id: int

    def __init__(self) -> None:
        self._charactersitcs: list[charactersitic] = []

    @abstractmethod
    def setup(self, peripheral: Peripheral) -> None:
        """Register this service and its charactersitics with bluezero"""
        raise NotImplementedError


class gatt_server:
    def __init__(self) -> None:
        self._adapter_address: str = list(adapter.Adapter.available())[0].address
        self._peripheral: Peripheral = Peripheral(self._adapter_address, "MyRobot")
        self._services: list[service] = []

    def start(self):
        """start sending out advertising packages"""
        self._peripheral.publish()

    def _setup_services(self):
        for service in self._services:
            service.setup(self._peripheral)

if __name__ == "__main__":
    gs = gatt_server()
    gs.start()
