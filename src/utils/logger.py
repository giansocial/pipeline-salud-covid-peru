import logging
import os


def get_logger(name):
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("[%(levelname)s] %(asctime)s - %(name)s: %(message)s",
                              datefmt="%H:%M:%S")
        )
        logger.addHandler(handler)

    logger.setLevel(getattr(logging, level, logging.INFO))
    return logger
