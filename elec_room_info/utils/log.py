import logging
import pathlib

# LOG_PATH = pathlib.Path("../data/logs/app.log")
LOG_PATH = pathlib.Path(__package__).absolute().parent / "data" / "logs" / "app.log"


def setup_logger(level):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(level=level,
                        format='%(asctime)s - %(levelname)s - %(name)s: %(message)s',
                        handlers=[logging.FileHandler(LOG_PATH),
                                  logging.StreamHandler()])


def get_logger(name):
    setup_logger(logging.DEBUG)
    return logging.getLogger(name)
