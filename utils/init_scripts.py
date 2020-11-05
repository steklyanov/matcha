import sys

import logging
import logging.config
import toml


def load_config(config_path: "config.toml") -> dict:
    try:
        with open("config.toml", 'r') as fh:
            logging.info('loading config file...')
            config = toml.load(fh)
    except FileNotFoundError:
        logging.error('config with name "{}" not found'.format(config_path))
        sys.exit(1)
    return config


def set_logging(config: dict):
    try:
        logging.config.dictConfig(config['logging'])
    except KeyError:
        logging.warning('no "logging" section, applying default logging settings')



