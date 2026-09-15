from ble.api.characteristic import Characteristic
from ble.api.flags import CharacteristicFlags

class CommandCharactersitics(Characteristic):
    service_id = 1
    characterstic_id = 1
    uuid = "1306f3ea-6fb6-48fa-84b9-b9575db45d0f"
    flags = [CharacteristicFlags.WRITE, CharacteristicFlags.READ]
    value = [0,0,0,0]
    notifying = False

    def update_value(self, value, options) -> bool | None:
        """Updates the characteristic value."""
        
        self.value = value

        speed: int = (value[0] << 8) | value [1]
        steering: int = (value[2] << 8) | value [3]

        print(f"Speed: {speed}, Steering: {steering}")
        return True

