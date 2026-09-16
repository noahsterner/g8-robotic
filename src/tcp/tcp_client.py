# file: ./src/tcp/tcp_client.py

import socket
import logging
import threading

logger = logging.getLogger(__name__)

class TcpClient:
    def __init__(self, host: str, port: int):
        self._host: str = host
        self._port: int = port
        self._socket: socket.socket | None = None
        self._lock: threading.Lock = threading.Lock()

    def connect(self) -> None:
        if not self._socket:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self._host, self._port))

            logger.info("Connected to tcp server: %s:%d", self._host, self._port)

    def request(self, message: str) -> bytearray:
        with self._lock:
            self._write(message)
            return self._recv()

    def _write(self, message: str) -> None:
        if not self._socket:
            raise RuntimeError("client not connected to a tcp socket")

        data: bytearray = bytearray((message + "\n").encode("utf-8"))
        self._socket.sendall(data)
        # logger.info("Write data to tcp socket: %s:%d", self._host, self._port)

    def _recv(self) -> bytearray:
        if not self._socket:
            raise RuntimeError("client not connected to a tcp socket")

        message: bytearray = bytearray()
        while True:
            byte: bytes = self._socket.recv(1)

            if len(byte) == 0:
                raise RuntimeError("client closed connection")

            if byte == b"\n":
                break

            message.extend(byte)

        # logger.info("Recieved data from tcp socket, %s:%d", self._host, self._port)
        return message

if __name__ == "__main__":
    client = TcpClient("localhost", 4711)
    client.connect()
    data = client.request("Hello, from xyz-robotic")
    print(data.decode("utf-8"))

