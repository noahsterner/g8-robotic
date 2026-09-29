# file: ./src/tcp/tcp_client.py

import socket
import logging
import threading
import time

logger = logging.getLogger(__name__)

class TcpClient:
    def __init__(self, host: str, port: int, retries: int = 10, retry_delay: float = 1.0):
        self._host: str = host
        self._port: int = port
        self._socket: socket.socket | None = None
        self._lock: threading.Lock = threading.Lock()
        self._retries: int = retries
        self._retry_delay: float = retry_delay

    def connect(self) -> None:
        with self._lock:
            if not self._socket:

                for attempt in range(1, self._retries + 1):
                    sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    
                    try:
                        sock.connect((self._host, self._port))
                    except:
                        sock.close()
                        logger.warning("Tcp connection attempt %d/%d failed", attempt, self._retries)

                        if attempt < self._retries:
                            time.sleep(self._retry_delay)

                        continue

                    self._socket = sock
                    logger.info("Connected to tcp server: %s:%d", self._host, self._port)
                    return

                raise RuntimeError(f"Failed to connect to {self._host}:{self._port}")
    
    def disconnect(self):
        if not self._socket:
            return

        try:
            self._socket.close()
        except:
            pass

        self._socket = None

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
    client.disconnect()

