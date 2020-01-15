#!/usr/bin/env python3

from time import sleep
from time import time
import logging

start = time()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('/home/robot/Teste/Logs/main.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(message)s'))
logger.addHandler(file_handler)

from alinhamento_inicial import alinhamento_meeting_area
from aprender_cores import aprender_cores
from achar_cor import achar_cor
from pegar_Cano import pegar_cano
import robo

elapsed = time() - start
logger.info("Time elapsed to importations = {} s".format(elapsed))

while True:
    if robo.btn.any():
        robo.sound.beep() 
        break
    else:
        sleep(0.01)

logger.info("Processso iniciado")
robo.rgbmax_esq = robo.definir_rgbmax('esq')
robo.rgbmax_dir = robo.definir_rgbmax('dir')

while True:
    alinhamento_meeting_area()
    logger.info("Alinhamento completo")
    aprender_cores()
    logger.info("Cores aprendidas")
    achar_cor()
    logger.info("Cor encontrada")
    pegar_cano()
    logger.info("Cano pego")