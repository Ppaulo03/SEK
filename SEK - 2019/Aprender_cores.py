from Robô import Robot
from time import sleep
import math
import os.path
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('reconhecer_cor.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(message)s'))
logger.addHandler(file_handler)

def autocompletar(cor1, cor2):
    A = {cor1, cor2}
    B = {'azul','vermelho','amarelo'}
    for item in (B-A):
        cor = item
    return cor

def aprender_cores(Kleiton):
    while True:
        h = os.path.exists("cores.txt")
        if h:
            mapa = [line.rstrip('\n') for line in open("cores.txt")] # pra ler o arquivo pra lista de novo
            Kleiton.set_mapa_de_cores(mapa)
            Kleiton.sound().beep()
            Kleiton.sound().beep()
            break
        else:
            Kleiton.steering_pair().on_for_degrees(0,-20,450)
            sleep(1)
            Kleiton.girar_pro_lado('esq',90)
            sleep(1)
            Kleiton.sound().beep()
            while Kleiton.cor('esq')!='vazio' and Kleiton.cor('dir')!='vazio':
                while Kleiton.cor('esq')=='branco' and Kleiton.cor('dir')=='branco':
                    Kleiton.steering_pair().on(0,25)
                else:
                    Kleiton.steering_pair().off()
                while Kleiton.cor('esq')!= 'branco' and Kleiton.cor('esq')!='vazio':
                    Kleiton.steering_pair().on(15,20)
                else:
                    Kleiton.steering_pair().off()
                while Kleiton.cor('dir')!= 'branco' and Kleiton.cor('dir')!='vazio':
                    Kleiton.steering_pair().on(-15,20)
                else:
                    Kleiton.steering_pair().off()
                    sleep(1)
            else:
                Kleiton.steering_pair().off()
                Kleiton.steering_pair().on_for_degrees(0,-20,120)
                Kleiton.alinhamento()
                sleep(1)
                Kleiton.steering_pair().on_for_degrees(0,-20,450)
                sleep(1)
                Kleiton.sound().beep()
                Kleiton.girar_pro_lado('dir',90)
                sleep(1)
            while Kleiton.cor('esq')!='vazio' and Kleiton.cor('dir')!='vazio':
                while Kleiton.cor('dir')!='amarelo' and Kleiton.cor('dir')!='vermelho' and Kleiton.cor('dir')!='azul':
                    Kleiton.steering_pair().on(0,20)
                else:
                    Kleiton.steering_pair().off()
                    cor1=Kleiton.cor('dir')
                    if cor1 != 'vermelho' and cor1!='amarelo' and cor1!='azul':
                        logger.error('cor1 inddentificada errada: cor1 = {}'.format(cor1))
                    break
            else:
                Kleiton.steering_pair().on_for_degrees(0,-20,150)
                Kleiton.girar_pro_lado('dir',20)
            while Kleiton.cor('dir')!='preto':
                Kleiton.steering_pair().on(90,10)
            else:
                Kleiton.steering_pair().off()
                Kleiton.sound().beep()
            while Kleiton.cor('esq')==cor1:
                while Kleiton.cor('dir') == cor1:
                    Kleiton.steering_pair().on(15,20)
                else:
                    Kleiton.steering_pair().off()
                while Kleiton.cor('dir') == 'preto':
                    Kleiton.steering_pair().on(0,20)
                else:
                    Kleiton.steering_pair().off()
                while Kleiton.cor('dir') != 'preto' and Kleiton.cor('dir') != cor1:
                    Kleiton.steering_pair().on(-15,20)
                else:
                    Kleiton.steering_pair().off()
                    cor2 = Kleiton.cor('esq')
                    if cor2 != 'vermelho' and cor2!='amarelo' and cor2!='azul':
                        logger.error('cor2 inddentificada errada: cor2 = {}'.format(cor2))
                    cor3 = autocompletar(cor1,cor2)   
            else:
                cores = open("cores.txt", "w+")     #cria o arquivo 
                escrever = [cor3,'\n',cor2,'\n',cor1]
                cores.writelines(escrever)
                cores.close()
                Kleiton.sound().beep()

if __name__ == '__main__':
    Kleiton = Robot()
    aprender_cores(Kleiton)