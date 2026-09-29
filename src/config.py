# file: ./src/config.py

import os

class Config:
    TCP_HOST: str = os.getenv("TCP_HOST", "127.0.0.1")
    TCP_PORT: int = int(os.getenv("TCP_HOST", "4711"))

    ROBOT_NAME: str = os.getenv("ROBOT_NAME", "MyRobot")
    
    ENABLE_TEST_MODE_INTERVAL: float = float(os.getenv("ENABLE_TEST_MODE_INTERVAL", "0.5"))
    KEEP_ALIVE_INTERVAL: float = float(os.getenv("KEEP_ALIVE_INTERVAL", "120"))
