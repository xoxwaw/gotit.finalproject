import os
import logging

from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '../../.env'))


def validate_env(name):
    var = None
    try:
        var = os.getenv(name)
    except EnvironmentError:
        logging.error('{} must be specified in .env file'.format(name))
        exit(0)
    return var