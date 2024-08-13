import logging


def setup_logger(level):
    logging.basicConfig(level=level,
                        format='%(asctime)s - %(levelname)s - %(name)s: %(message)s',
                        handlers=[logging.FileHandler('../app.log'),
                                  logging.StreamHandler()])


def get_logger(name):
    setup_logger(logging.DEBUG)
    return logging.getLogger(name)
