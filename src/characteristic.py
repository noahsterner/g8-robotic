from dataclasses import dataclass
from typing import Any

from bluezero.peripheral import Peripheral

class Characteristic:
    """Base class for a GATT characteristic.

    A characteristics belongs to a service and defines the behaviour for reading, writing and notifications.
    """
    srv_id: int
    chr_id: int
    uuid: str
    flags: list[str]
    value: list[Any]
    notifying: bool

    def read_value(self) -> list[int] | None:
        """Reads the value of the characteristic

        Return the characteristic value as a list of uint8 values.
        """
        return None

    def update_value(self, value, options) -> bool | None:
        """Updates the characteristic value."""
        return None

    def notify(self, notifying: bool) -> None:
        """Toggle notifications."""
        return None

    def setup(self, peripheral: Peripheral) -> None:
        peripheral.add_characteristic(
                srv_id = self.srv_id,
                chr_id = self.chr_id,
                uuid = self.uuid,
                value = self.value,
                flags = self.flags,
                notifying = self.notifying,
                read_callback = self.read_value,
                write_callback = self.update_value,
                notify_callback = self.notify,
        )

