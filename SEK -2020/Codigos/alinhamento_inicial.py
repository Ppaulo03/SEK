#!/usr/bin/env python3
import robo
import math
import logging
from time import sleep

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('/home/robot/Codigos/Logs/reconhecer_cor.log')
file_handler.setFormatter(logging.Formatter('%(name)s:%(message)s'))
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

def sair_da_meeting_area():
    while robo.cor('esq')=='branco' and robo.cor('dir')=='branco':
        robo.steering_pair.on(0,20)
    else:
        robo.steering_pair.off()
            
def no_vazio():
    robo.steering_pair.on_for_degrees(0,-10,80)
    sleep(1)
    robo.alinhamento()
    sleep(1)
    robo.steering_pair.on_for_degrees(0,-10,350)
    sleep(1)
    robo.girar_pro_lado('esq',90)
    sleep(1)

def algum_preto():
    robo.steering_pair.on_for_degrees(0,-10,120)
    robo.alinhamento()
    robo.sound.beep()
    robo.steering_pair.on_for_degrees(0,-10,120)
    sleep(1)
    robo.sound.beep()
    robo.alinhamento()
    logger.debug("fim do algum preto")
    return

def alinhamento_meeting_area():
    while True:
        logger.debug("Andando no branco")
        while robo.cor('esq')=='branco' and robo.cor('dir')=='branco':
            robo.steering_pair.on(0,10)
        else:
            logger.debug("Um sensor saiu do branco (E/D)")
            logger.debug(robo.cor('esq'))
            logger.debug(robo.cor('dir'))
            robo.steering_pair.off() 
        if robo.cor('esq')=='vazio' or robo.cor('dir')=='vazio':
            logger.debug("No vazio")
            no_vazio()
        else:
            logger.debug("Alinhar pra testar o preto")
            # algum_preto()
            robo.steering_pair.on_for_degrees(0,-10,120)
            robo.alinhamento()
            robo.sound.beep()
            robo.steering_pair.on_for_degrees(0,-10,120)
            sleep(1)
            robo.sound.beep()
            robo.alinhamento()
            sleep(1)
            logger.debug("Vamos testar se é preto ou rampa")
            if robo.testar_preto():
                logger.debug("Parabéns! Achou a linha preta")
                while robo.cor('esq')!='branco' or robo.cor('dir')!='branco':
                    robo.steering_pair.on(0,-15)
                else:
                    logger.debug("Alinhar na borda")
                    robo.steering_pair.off()
                    robo.steering_pair.on_for_degrees(0,-20,80)
                    robo.alinhamento()
                    robo.sound.beep()
                    logger.debug("Alinhoooooou caralho")
                    return
            else:
                logger.debug("Que pena, é uma rampa. Meia volta")
                robo.steering_pair.on_for_degrees(0,-10,350)
                robo.girar_pro_lado('esq',180)

if __name__ == '__main__':
    robo.rgbmax_dir = robo.definir_rgbmax('dir')
    robo.rgbmax_esq = robo.definir_rgbmax('esq')
    alinhamento_meeting_area()