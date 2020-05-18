from Robô import Robot
from time import sleep
import math
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('reconhecer_cor.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(message)s'))
logger.addHandler(file_handler)

def sair_da_meeting_area(Kleiton):
    while Kleiton.cor('esq')=='branco' and Kleiton.cor('dir')=='branco':
        Kleiton.steering_pair().on(0,20)
    else:
        Kleiton.steering_pair().off()
            
def no_vazio(Kleiton):
    Kleiton.steering_pair().on_for_degrees(0,-10,80)
    sleep(1)
    Kleiton.alinhamento()
    sleep(1)
    Kleiton.steering_pair().on_for_degrees(0,-10,350)
    sleep(1)
    Kleiton.girar_pro_lado('esq',90)
    sleep(1)

def algum_preto(Kleiton):
    Kleiton.steering_pair().on_for_degrees(0,-10,120)
    Kleiton.alinhamento()
    Kleiton.sound().beep()
    Kleiton.steering_pair().on_for_degrees(0,-10,120)
    sleep(1)
    Kleiton.sound().beep()
    Kleiton.alinhamento()
    sleep(1)

def alinhamento_meeting_area(Kleiton):
    while True:
        if Kleiton.cor('esq')=='vazio' or Kleiton.cor('dir')=='vazio':
            no_vazio(Kleiton)
        else:
            algum_preto(Kleiton)
            if Kleiton.testar_preto():
                while Kleiton.cor('esq')!='branco' or Kleiton.cor('dir')!='branco':
                    Kleiton.steering_pair().on(0,-15)
                else:
                    Kleiton.steering_pair().off()
                    Kleiton.steering_pair().on_for_degrees(0,-20,80)
                    Kleiton.alinhamento()
                    Kleiton.sound().beep()
                break
            else:
                Kleiton.steering_pair().on_for_degrees(0,-10,350)
                Kleiton.girar_pro_lado('esq',180)

if __name__ == '__main__':
    Kleit = Robot()
    alinhamento_meeting_area(Kleit)