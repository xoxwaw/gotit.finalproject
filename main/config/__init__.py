import logging
import os
from importlib import  import_module


def get_env(name):
    var = os.getenv(name)
    if var is None:
        logging.error('{} must be specified in .env file'.format(name))
        exit(1)
    return var


def load(env):
    module = None
    try:
        module = import_module('main.config.{}'.format(env))
    except ModuleNotFoundError:
        logging.error('Environment {} not found'.format(env))
        exit(1)
    Config = getattr(module, 'Config')
    return Config()


conf = load(os.getenv('ENV'))
