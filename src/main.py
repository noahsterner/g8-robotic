from abc import abstractmethod
from typing import Any

from bluezero import async_tools
from bluezero.peripheral import Peripheral
from bluezero import adapter

class Service:
    """Base class for a GATT service.

    A service owns its own charactersitics and provides the callbacks required by bluezero
    """
    def __init__(self) -> None:
        self._charactersitcs: list[Any] = []

    @abstractmethod
    def setup(self) -> None:
        """Register this service and its charactersitics wit bluezero"""
        raise NotImplementedError

    def read_value(self) -> None:
        """Called when a BLE clients reads a charactersitics"""
        raise NotImplementedError

    def update_value(self, charactersitics) -> None:
        """Called when a BLE central updates a charactersitics value"""
        raise NotImplementedError

    def notify(self, notifying, charactersitics) -> None:
        """Called when a BLE central subscribes/unsubscribse from charactersitics notification"""
        pass

class gatt_server:
    def __init__(self) -> None:
        self._adapter_address: str = list(adapter.Adapter.available())[0].address
        self._peripheral: Peripheral = Peripheral(self._adapter_address, "MyRobot")
        self._services: list[Service] = []
    def start(self):
        """start sending out advertising packages"""
        self._peripheral.publish()

if __name__ == "__main__":
    gs = gatt_server()
    gs.start()
