# file: ./src/main.py

import logging, threading, time

from dotenv import load_dotenv

from logger_config import setup_logger
from config import Config

from ble.services.command_service import CommandService
from ble.services.battery_service import BatteryService
from ble.api.gatt_server import GattServer
from tcp.tcp_client import TcpClient
from tcp.tcp_client import TcpClient
from autoDrive.autodrive import AutoDrive
from core.robot import Robot

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
    load_dotenv()
    setup_logger()


    tcp_client = TcpClient(Config.TCP_HOST, Config.TCP_PORT)
    tcp_client.connect()

    # initialize autodrive and robot class
    # how to link the button im unsure if this is in main or elsewhere
    robot: Robot = Robot(tcp_client)
    autoDrive = AutoDrive(robot)

    threading.Thread(target=enable_test_mode, kwargs={"delay": Config.ENABLE_TEST_MODE_INTERVAL, "tcp_client": tcp_client}).start()
    threading.Thread(target=keep_alive, kwargs={"delay": Config.KEEP_ALIVE_INTERVAL, "tcp_client": tcp_client}).start()

    gatt_server = GattServer(name = Config.ROBOT_NAME, services = [
        CommandService(robot),
        BatteryService(robot)
    ]).start()

if __name__ == "__main__":
    main()
