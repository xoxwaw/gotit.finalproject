import logging
import os


def get_env(name):
    var = os.getenv(name)
    if var is None:
        logging.error('{} must be specified in .env file'.format(name))
        exit(1)
    return var
