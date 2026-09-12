from service import Service

from bluezero.peripheral import Peripheral
from bluezero import adapter

class GattServer:
    def __init__(self) -> None:
        self._adapter_address: str = list(adapter.Adapter.available())[0].address
        self._peripheral: Peripheral = Peripheral(self._adapter_address, "MyRobot")
        self._services: list[Service] = []

    def start(self):
        """start sending out advertising packages"""
        self._peripheral.publish()

    def _setup_services(self):
        for service in self._services:
            service.setup(self._peripheral)
