# file: ./src/logger_config.py

import logging, os
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logger() -> None:
    console_level: str = os.getenv("LOG_CONSOLE_LEVEL", "INFO").upper()
    file_level: str = os.getenv("LOG_FILE_LEVEL", "DEBUG").upper()

    file: str = os.getenv("LOG_FILE", "logs/robot.log")
    max_bytes: int = int(os.getenv("LOG_MAX_BYTES", "10000000"))
    backup_count: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    
    Path(file).parent.mkdir(exist_ok=True)

    console_handler: logging.StreamHandler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    
    file_handler: RotatingFileHandler = RotatingFileHandler(file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setLevel(file_level)
    
    logging.basicConfig(
        level = logging.INFO,
        format = "[%(levelname)s] [%(asctime)s] [file: %(filename)s] [thread: %(threadName)s] | %(message)s",
        handlers=[
            console_handler,
            file_handler,
        ]
    )

    loggin.getLogger("bluzero").disabled = True
