"""
This module contains the setup_logging function, which
configures logging for the e-wallet application.

Dependencies:
    - logging
    - sys

Functions:
    - setup_logging(): configures logging for the e-wallet application.

"""

import logging
import sys


def setup_logging():
    """
    Set up logging configuration for the e-wallet application.

    This function configures logging to write messages to a file located at 'logs/e-wallet.log'.
    It also sets the encoding to 'utf-8', logging level to 'DEBUG', and formats log messages
    to include the timestamp, log level, logger name, thread name, and log message.

    Additionally, this function adds a console handler to the root logger to print log messages
    to the console.

    """
    logging.basicConfig(
        filename="logs/e-wallet.log",
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
        )
    )
    logging.getLogger().addHandler(console_handler)
