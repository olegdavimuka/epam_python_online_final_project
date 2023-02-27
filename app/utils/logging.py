import logging
import sys

def setup_logging():
    logging.basicConfig(
        filename="logs/e-wallet.log",
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
    )
    logging.getLogger().addHandler(console_handler)