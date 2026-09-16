import logging, threading, time
from logger_config import setup_logger

from ble.services.command_service import CommandService
from ble.services.battery_service import BatteryService
from ble.api.gatt_server import GattServer
from tcp.tcp_client import TcpClient

logger = logging.getLogger(__name__)

# This need to move elsewhere, keep it here for know
def enable_test_mode(tcp_client: TcpClient, delay: int):
    while True:
        tcp_client.request("SafetySupervisor.EnableTestMode()")
        time.sleep(0.5)

# This need to move elsewhere, keep it here for know
def keep_alive(tcp_client: TcpClient, delay):
    while True:
        tcp_client.request("SystemPower.KeepAlive()")
        time.sleep(delay)

def main():
    setup_logger()

    tcp_client = TcpClient("localhost", 4711)
    tcp_client.connect()

    threading.Thread(target=enable_test_mode, kwargs={"delay": 1, "tcp_client": tcp_client}).start()
    threading.Thread(target=keep_alive, kwargs={"delay": 120, "tcp_client": tcp_client}).start()

    gatt_server = GattServer(name = "MyRobot", services = [
        CommandService(tcp_client),
        BatteryService(tcp_client)
    ]).start()

if __name__ == "__main__":
    main()
