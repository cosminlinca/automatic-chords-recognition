import logging
import logging.config
import yaml

LOGGING_FILE_PATH = 'F://Licenta//BE.Automatic.Chords.Recognition//src//logging.yml'


def logging_setup():
    with open(LOGGING_FILE_PATH, 'r') as f:
        config = yaml.safe_load(f.read())
        # Config logging using a dictionary
        logging.config.dictConfig(config)
