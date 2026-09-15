import logging
from abc import update_abstractmethods

from bluezero.localGATT import async_tools

from ble.api import characteristic
from ble.api.characteristic import Characteristic
from ble.api.flags import CharacteristicFlags
from tcp.tcp_client import TcpClient

logger = logging.getLogger()

class BatteryLevelCharacteristics(Characteristic):
    service_id = 2
    characteristic_id = 1
    uuid = "0000180F-0000-1000-8000-00805F9B34FB"
    flags = [CharacteristicFlags.READ, CharacteristicFlags.NOTIFY]
    notifying = False
    value = [0]

    def __init__(self, tcp_client: TcpClient) -> None:
        super().__init__(tcp_client)

    def read_value(self) -> list[int] | None:
        data = self._tcp_client.request("Battery.GetBatteryLevel()")
        self.value[0] = list(data)
        return list(self.value)

    def notify(self, notifying: bool, characteristic) -> None:
        self.notifying = notifying
        
        logger.info("Notification: %s", self.notifying)

        if self.notifying:
            logger.info("Start notification timer")
            async_tools.add_timer_seconds(2, self._update_value, characteristic)

    def _update_value(self, characteristic) -> bool | None:
        if not self.notifying:
            logger.info("Notification disabled, stopped timer")

        new_data = self.read_value()
        characteristic.set_value(new_data)

        logger.info("Battery level: %s%", new_data)
        return self.notifying
