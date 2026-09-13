import logging, os

def setup_logger() -> None:
    level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    file: str = os.getenv("LOG_FILE", "robot.log")

    logging.basicConfig(
            level = level,
            format = "[%(levelname)s] [%(asctime)s] [file: %(filename)s] [thread: %(threadName)s] | %(message)s",
            handlers=[
                logging.FileHandler(file)
                ]
            )
