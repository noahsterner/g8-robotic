from abc import ABC, abstractmethod

from bluezero.peripheral import Peripheral

from characteristic import Charactersitic

class Service(ABC):
    """Base class for a GATT service.

    A service owns its own charactersitics and are responsible for registering them
    """

    uuid: str
    srv_id: int

    def __init__(self) -> None:
        self._charactersitcs: list[Charactersitic] = []

    @abstractmethod
    def setup(self, peripheral: Peripheral) -> None:
        """Register this service and its charactersitics with bluezero"""
        raise NotImplementedError


