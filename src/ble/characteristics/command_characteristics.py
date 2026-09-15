from ble.api.characteristic import Characteristic
from ble.api.flags import CharacteristicFlags
from tcp.tcp_client import TcpClient

class CommandCharactersitics(Characteristic):
    service_id = 1
    characterstic_id = 1
    uuid = "1306f3ea-6fb6-48fa-84b9-b9575db45d0f"
    flags = [CharacteristicFlags.WRITE]
    value = [0,0,0,0]
    notifying = False

    def __init__(self, tcp_client: TcpClient) -> None:
        super().__init__(tcp_client)

    def update_value(self, value, options) -> bool | None:
        """Updates the characteristic value."""

        self.value = value

        speed: int = (self.value[0] << 8) | self.value [1]
        steering: int = (self.value[2] << 8) | self.value [3]
    
        print(speed, steering)
        self._tcp_client.request(f"Driver.Drive(speed:{speed}, steering:{steering})")
        #time.sleep(60)
        return True

