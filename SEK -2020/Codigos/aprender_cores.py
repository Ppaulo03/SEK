#!/usr/bin/env python3
import robo
import math
import os.path
import logging
from time import sleep

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('/home/robot/Teste/Codigos/reconhecer_cor.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(message)s'))
logger.addHandler(file_handler)

def autocompletar(cor1, cor2):
    A = {cor1, cor2}
    B = {'azul','vermelho','amarelo'}
    for item in (B-A):
        cor = item
    return cor

def aprender_cores():
    while True:
        h = os.path.exists("cores.txt")
        if h:
            mapa = [line.rstrip('\n') for line in open("cores.txt")] # pra ler o arquivo pra lista de novo
            robo.mapa_de_cores = mapa
            robo.sound.beep()
            robo.sound.beep()
            break
        else:
            robo.steering_pair.on_for_degrees(0,-20,450)
            sleep(1)
            robo.girar_pro_lado('esq',90)
            sleep(1)
            robo.sound.beep()
            while robo.cor('esq')!='vazio' and robo.cor('dir')!='vazio':
                while robo.cor('esq')=='branco' and robo.cor('dir')=='branco':
                    robo.steering_pair.on(0,25)
                else:
                    robo.steering_pair.off()
                while robo.cor('esq')!= 'branco' and robo.cor('esq')!='vazio':
                    robo.steering_pair.on(15,20)
                else:
                    robo.steering_pair.off()
                while robo.cor('dir')!= 'branco' and robo.cor('dir')!='vazio':
                    robo.steering_pair.on(-15,20)
                else:
                    robo.steering_pair.off()
                    sleep(1)
            else:
                robo.steering_pair.off()
                robo.steering_pair.on_for_degrees(0,-20,120)
                robo.alinhamento()
                sleep(1)
                robo.steering_pair.on_for_degrees(0,-20,450)
                sleep(1)
                robo.sound.beep()
                robo.girar_pro_lado('dir',90)
                sleep(1)
            while robo.cor('esq')!='vazio' and robo.cor('dir')!='vazio':
                while robo.cor('dir')!='amarelo' and robo.cor('dir')!='vermelho' and robo.cor('dir')!='azul':
                    robo.steering_pair.on(0,20)
                else:
                    robo.steering_pair.off()
                    cor1=robo.cor('dir')
                    if cor1 != 'vermelho' and cor1!='amarelo' and cor1!='azul':
                        logger.error('cor1 inddentificada errada: cor1 = {}'.format(cor1))
                    break
            else:
                robo.steering_pair.on_for_degrees(0,-20,150)
                robo.girar_pro_lado('dir',20)
            while robo.cor('dir')!='preto':
                robo.steering_pair.on(90,10)
            else:
                robo.steering_pair.off()
                robo.sound.beep()
            while robo.cor('esq')==cor1:
                while robo.cor('dir') == cor1:
                    robo.steering_pair.on(15,20)
                else:
                    robo.steering_pair.off()
                while robo.cor('dir') == 'preto':
                    robo.steering_pair.on(0,20)
                else:
                    robo.steering_pair.off()
                while robo.cor('dir') != 'preto' and robo.cor('dir') != cor1:
                    robo.steering_pair.on(-15,20)
                else:
                    robo.steering_pair.off()
                    cor2 = robo.cor('esq')
                    if cor2 != 'vermelho' and cor2!='amarelo' and cor2!='azul':
                        logger.error('cor2 inddentificada errada: cor2 = {}'.format(cor2))
                    cor3 = autocompletar(cor1,cor2)   
            else:
                cores = open("cores.txt", "w+")     #cria o arquivo 
                escrever = [cor3,'\n',cor2,'\n',cor1]
                cores.writelines(escrever)
                cores.close()
                robo.sound.beep()

if __name__ == '__main__':
    aprender_cores()