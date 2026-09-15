# file: ./src/ble/api/gatt_server.py

import logging

from bluezero.device import Device
from bluezero.peripheral import Peripheral
from bluezero import adapter

from ble.api.service import Service

logger = logging.getLogger(__name__)

class GattServer:
    def __init__(self, name: str, services: list[Service]) -> None:
        self._adapter_address: str = list(adapter.Adapter.available())[0].address
        self._peripheral: Peripheral = Peripheral(self._adapter_address, local_name=name)
        self._services: list[Service] = services

    def start(self) -> None:
        """start sending out advertising packages"""
        logger.info("Start GATT Server")

        self._peripheral.on_connect = self._on_connect
        self._peripheral.on_disconnect = self._on_disconnect

        self._peripheral.advert.manufacturer_data(0x0000, [0x000000])

        self._setup_services()
        self._peripheral.publish()

    def _setup_services(self) -> None:
        """Set up and register all services on the peripheral"""
        logger.info("Setup GATT services and its characteristics")

        for service in self._services:
            service.setup(self._peripheral)

    def _on_connect(self, device: Device) -> None:
        logger.info("Central connected: %s", device)

    def _on_disconnect(self, adapter_address: str, device_address: str) -> None:
        logger.info("Central disconnected: %s, %s", adapter_address, device_address)
