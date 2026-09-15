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
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self._host, self._port))

            logger.info("Connected to tcp server: %s:%d", self._host, self._port)

    def _write(self, message):
        if not self._socket:
            raise RuntimeError("client not connected to a tcp socket")

        data = bytearray((message + "\n").encode("utf-8"))
        self._socket.sendall(data)

    def _recv(self) -> bytearray:
        if not self._socket:
            raise RuntimeError("client not connected to a tcp socket")

        message = bytearray()
        while True:
            byte = self._socket.recv(1)

            if byte == b"\n":
                break

            message.extend(byte)

        return message

if __name__ == "__main__":
    client = TcpClient("localhost", 4711)
    client.connect()
    client._write("Hello, from xyz-robotic")
    recv = client._recv().decode("utf-8")
    print(recv)

