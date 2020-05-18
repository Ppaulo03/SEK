from Robô import Robot
from time import sleep
import math
import os.path
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('achar_cor.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(message)s'))
logger.addHandler(file_handler)

def achar_cor(Kleiton):
    Kleiton.sound().beep()
    ordem = Kleiton.get_tamanho()
    mapa = Kleiton.get_mapa_de_cores()
    cor_desejada =ordem[Kleiton.get_index()]
    cor_estou = Kleiton.cor('esq')
    indice_cor_desejada = mapa.index(cor_desejada)
    indice_cor_estou = mapa.index(cor_estou)
    if indice_cor_estou == indice_cor_desejada:
        pass #pq já vai pra pegar_um_cano abaixo
    elif indice_cor_estou > indice_cor_desejada:
        while Kleiton.cor('esq')!=cor_desejada:
            Kleiton.steering_pair().on(0,15)
        else:
            Kleiton.steering_pair().off()
            #e vai pegar cano
    elif indice_cor_desejada != 2:
        while Kleiton.cor('esq')!=mapa[indice_cor_desejada+1]: #voltar seguindo a linha preta
            while Kleiton.cor('dir') == mapa[0]:
                Kleiton.steering_pair().on(15,-20)
            else:
                Kleiton.steering_pair().off()
            while Kleiton.cor('dir') == 'preto':
                Kleiton.steering_pair().on(0,-20)
            else:
                Kleiton.steering_pair().off()
            while Kleiton.cor('dir') != 'preto' and Kleiton.cor('dir') != mapa[0]:
                Kleiton.steering_pair().on(-15,-20)
            else:
                Kleiton.steering_pair().off()   
        else:
            Kleiton.steering_pair().off()
    elif indice_cor_desejada == 2:
        Kleiton.girar_pro_lado('dir',180)
            #ir até o vazio, alinhar, virar e voltar
    Kleiton.sound().beep()

if __name__ == '__main__':
    Kleiton = Robot()
    achar_cor(Kleiton)
