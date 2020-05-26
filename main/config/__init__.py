import os
import logging

from dotenv import load_dotenv


load_dotenv()


def validate_env(name):
    var = None
    try:
        var = os.getenv(name)
    except EnvironmentError:
        logging.error('{} must be specified in .env file'.format(name))
        exit(0)
    return var