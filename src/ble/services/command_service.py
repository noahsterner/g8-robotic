from ble.api.service import Service
from ble.api.characteristic import Characteristic
from ble.characteristics.command_characteristics import CommandCharactersitics

class CommandService(Service):
    @property
    def characteristics(self) -> list[Characteristic]:
        return [CommandCharactersitics()]

    @property
    def uuid(self) -> str:
        return "f1204501-027a-4d8d-8704-8cb352456dc7"

    @property
    def service_id(self) -> int:
        return 1
