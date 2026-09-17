import logging
from bluezero import async_tools
from ble.api.characteristic import Characteristic
from ble.api.flags import CharacteristicFlags
from tcp.tcp_client import TcpClient

logger = logging.getLogger(__name__)

class BatteryLevelCharacteristic(Characteristic):
    characteristic_id = 1
    uuid = "FF11"
    flags = [CharacteristicFlags.READ, CharacteristicFlags.NOTIFY]
    value = [100]
    notifying = False

    def __init__(self, tcp_client: TcpClient, service_id: int) -> None:
        super().__init__(tcp_client, service_id)

    def read_value(self) -> list[int]:
        self.value[0] = self._tcp_client.request("Battery.GetBatteryLevel()")
        logger.info("read battery level: %s", self.value)

        return self.value

    def notify(self, notifying: bool, characteristic) -> None:
        self.notifying = notifying
        if(self.notifying):
            async_tools.add_timer_seconds(10, self._pool_battery_level)

    def _pool_battery_level(self):
        self.value[0] = self._tcp_client.request("Battery.GetBatteryLevel()")
        logger.info("battery level pooled: %s", self.value)



