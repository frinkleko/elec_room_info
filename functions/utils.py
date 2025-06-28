import logging
import os
from dotenv import load_dotenv

# Load environment variables from the `.env` file
load_dotenv()


def get_logger(name):
    """
    Configure and return a logger for debug and info logging.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class Config:
    @staticmethod
    def get(key, default=None):
        """
        Fetches environment variables managed via `.env` file.
        Key lookups are case-sensitive.

        :param key: The environment variable name.
        :param default: An optional default value if the variable is not found.
        :return: The value of the environment variable or the default value.
        """
        return os.getenv(key, default)
