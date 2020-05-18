#!/usr/bin/env python3
import robo
import math
import os.path
import logging
from time import sleep

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('/home/robot/Teste/Codigos/achar_cor.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(message)s'))
logger.addHandler(file_handler)

def achar_cor():
    robo.sound.beep()
    ordem = robo.tamanhos
    mapa = robo.mapadecores
    cor_desejada =ordem[robo.item_lista]
    cor_estou = robo.cor('esq')
    indice_cor_desejada = mapa.index(cor_desejada)
    indice_cor_estou = mapa.index(cor_estou)
    if indice_cor_estou == indice_cor_desejada:
        pass #pq já vai pra pegar_um_cano abaixo
    elif indice_cor_estou > indice_cor_desejada:
        while robo.cor('esq')!=cor_desejada:
            robo.steering_pair.on(0,15)
        else:
            robo.steering_pair.off()
            #e vai pegar cano
    elif indice_cor_desejada != 2:
        while robo.cor('esq')!=mapa[indice_cor_desejada+1]: #voltar seguindo a linha preta
            while robo.cor('dir') == mapa[0]:
                robo.steering_pair.on(15,-20)
            else:
                robo.steering_pair.off()
            while robo.cor('dir') == 'preto':
                robo.steering_pair.on(0,-20)
            else:
                robo.steering_pair.off()
            while robo.cor('dir') != 'preto' and robo.cor('dir') != mapa[0]:
                robo.steering_pair.on(-15,-20)
            else:
                robo.steering_pair.off()   
        else:
            robo.steering_pair.off()
    elif indice_cor_desejada == 2:
        robo.girar_pro_lado('dir',180)
            #ir até o vazio, alinhar, virar e voltar
    robo.sound.beep()

if __name__ == '__main__':
    achar_cor()
