import logging
from logger_config import setup_logger

logger = logging.getLogger(__name__)

def main():
    setup_logger()
    logger.info("test")

if __name__ == "__main__":
    main()
