import logging
import os

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


def validate_env(name):
    var = os.getenv(name)
    if var is None:
        logging.error('{} must be specified in .env file'.format(name))
        exit(1)
    return var
