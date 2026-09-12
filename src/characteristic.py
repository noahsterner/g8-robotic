from dataclasses import dataclass
from typing import Any

@dataclass 
class Charactersitic:
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

    def update_value(self, charactersitics: Charactersitic) -> bool:
        """Updates the characteristic value."""
        raise NotImplementedError

    def notify(self, notifying: bool, charactersitic: Charactersitic) -> None:
        """Toggle notifications."""
        raise NotImplementedError

