import logging, threading, time
from logger_config import setup_logger

from ble.services.command_service import CommandService
from ble.services.battery_service import BatteryService
from ble.api.gatt_server import GattServer
from tcp.tcp_client import TcpClient
<<<<<<< HEAD
from tcp.tcp_client import TcpClient
from autoDrive.autodrive import AutoDrive
=======
>>>>>>> 957bc37 (feat(feature/ble): connect robot through DI to charactersitcs)
from core.robot import Robot
from core.battery import Battery

logger = logging.getLogger(__name__)

# This need to move elsewhere, keep it here for know
def enable_test_mode(tcp_client: TcpClient, delay: float):
    while True:
        tcp_client.request("SafetySupervisor.EnableTestMode()")
        time.sleep(delay)

# This need to move elsewhere, keep it here for know
def keep_alive(tcp_client: TcpClient, delay):
    while True:
        tcp_client.request("SystemPower.KeepAlive()")
        time.sleep(delay)

def main():
    setup_logger()

    tcp_client = TcpClient("localhost", 4711)
    tcp_client.connect()
    # initialize autodrive and robot class
    # how to link the button im unsure if this is in main or elsewhere
    robot = Robot(tcp_client)
    autoDrive = AutoDrive(robot)

    robot: Robot = Robot(tcp_client)
    battery: Battery = Battery(tcp_client)

    threading.Thread(target=enable_test_mode, kwargs={"delay": 0.5, "tcp_client": tcp_client}).start()
    threading.Thread(target=keep_alive, kwargs={"delay": 120, "tcp_client": tcp_client}).start()

    gatt_server = GattServer(name = "MyRobot", services = [
        CommandService(robot),
        BatteryService(battery)
    ]).start()

if __name__ == "__main__":
    main()
