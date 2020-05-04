# coding: utf-8
import sys
import os
import logging
from logging import StreamHandler, Formatter
from logging.handlers import RotatingFileHandler

from . import config

import logging
import logging.config
import yaml

with open("logging.yaml", 'rt') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger('PANDEMIC')