import logging
import pathlib

LOG_PATH = pathlib.Path("data/logs/app.log")


def setup_logger(level):
    logging.basicConfig(level=level,
                        format='%(asctime)s - %(levelname)s - %(name)s: %(message)s',
                        handlers=[logging.FileHandler(LOG_PATH),
                                  logging.StreamHandler()])


def get_logger(name):
    setup_logger(logging.DEBUG)
    return logging.getLogger(name)
