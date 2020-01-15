#!/usr/bin/env python3
import robo
import math
import logging
from time import sleep

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('/home/robot/Teste/Logs/reconhecer_cor.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(message)s'))
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
    sleep(1)

def alinhamento_meeting_area():
    while True:
        if robo.cor('esq')=='vazio' or robo.cor('dir')=='vazio':
            no_vazio()
        else:
            algum_preto()
            if robo.testar_preto():
                while robo.cor('esq')!='branco' or robo.cor('dir')!='branco':
                    robo.steering_pair.on(0,-15)
                else:
                    robo.steering_pair.off()
                    robo.steering_pair.on_for_degrees(0,-20,80)
                    robo.alinhamento()
                    robo.sound.beep()
                break
            else:
                robo.steering_pair.on_for_degrees(0,-10,350)
                robo.girar_pro_lado('esq',180)

if __name__ == '__main__':
    alinhamento_meeting_area()