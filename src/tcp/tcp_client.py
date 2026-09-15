# file: ./src/tcp/tcp_client.py

import socket
import logging

logger = logging.getLogger(__name__)

class TcpClient:
    def __init__(self, host: str, port: int):
        self._host: str = host
        self._port: int = port
        self._socket: socket.socket | None = None

    def connect(self):
        if not self._socket:
            logger.info("Connected to tcp server: %s:%d", self._host, self._port)
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self._host, self._port))

if __name__ == "__main__":
    client = TcpClient("localhost", 4711)
    client.connect()
