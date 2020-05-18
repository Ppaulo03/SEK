#!/usr/bin/env python3
import robo
import logging
from time import sleep

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('/home/robot/Codigos/Logs/reconhecer_cor.log')
file_handler.setFormatter(logging.Formatter('%(name)s:%(message)s'))
logger.addHandler(file_handler)

