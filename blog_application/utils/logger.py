import logging
import os
import threading
import multiprocessing
from datetime import datetime


# file_path = "C:\test\vitr-testing-vat-compliance\gc-automation\logs"
# log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
# file_handler = logging.FileHandler(log_filename)


def setup_logger(name):
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] [Thread:%(thread)d] %(funcName)s:%(filename)s %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    # Create a handler for console logging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Create a handler for file logging with a timestamp in the filename
    # file_handler.setFormatter(formatter)

    # Create a logger and add handlers
    logger = logging.getLogger(name)
    logger.addHandler(console_handler)
    # logger.addHandler(file_handler)

    logger.setLevel(logging.DEBUG)  # You can set the desired logging level here

    return logger
