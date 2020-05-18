from Robô import Robot
from time import sleep
import math
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('pegar_cano.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(message)s'))
logger.addHandler(file_handler)

Kleiton = Robot()
dist_maxima = 45

def distancia_min(sensor):
    cont=0
    distancia = []
    while(cont<=10):
        distancia[cont] = sensor.distance_centimeters
        sleep(0.05)
        cont+=1
    else:
        return min(distancia)

def reposicionar_garra(Kleiton):
    Kleiton.garra_g().on_for_seconds(100, 2)
    sleep(1)
    Kleiton.garra_m().on_for_degrees(60, 200)
    Kleiton.garra_g().on_for_degrees(40, 32*(-10))
    sleep(3)

def achar_cano(Kleiton):
    while (distancia_min(Kleiton.usl()) > dist_maxima): 
        Kleiton.steering_pair().on(0, 20)

    else:
        Kleiton.steering_pair().off()
        sleep(1)

def alinhar_com_cano(Kleiton):
    distancia = Kleiton.usl().distance_centimeters
    
    if(distancia > dist_maxima):
        logger.warning('Distância_1 maior que a distância máxima\n Distância = {}'.format(distancia))
    else:
        logger.debug('Distância_1 = {}'.format(distancia))
    
    Kleiton.girar_pro_lado("esq",90)
    sleep(1)
    Kleiton.steering_pair().on_for_degrees(0, 15, 32*(distancia/2))
    sleep(1)
    Kleiton.girar_pro_lado("dir",90)
    while (distancia_min(Kleiton.usl()) > dist_maxima - (distancia/2)):
        Kleiton.steering_pair().on(0, 20)

    else:
        Kleiton.steering_pair().off()

    while (distancia_min(Kleiton.usl()) < dist_maxima - distancia/2):
                Kleiton.steering_pair().on(0, 20)

    else:
        Kleiton.steering_pair().off() 
        Kleiton.steering_pair().on_for_degrees(0, -15, 32*(6))

def empurrar_cano(Kleiton):
    Kleiton.girar_pro_lado("esq",90)

    if(Kleiton.usf().distance_centimeters > dist_maxima):
        logger.warning('Distância frontal maior que a distância máxima\n Distância = {}'.format(Kleiton.usf().distance_centimeters))
    else:
        logger.debug('Distância frontal = {}'.format(Kleiton.usf().distance_centimeters))

    while(Kleiton.usf().distance_centimeters > 7):
        Kleiton.steering_pair().on(0, 15)
        sleep(0.3)

    else:
        Kleiton.steering_pair().off()
        Kleiton.steering_pair().on_for_seconds(0,20, 1) 
        sleep(0.5)
    
    while(Kleiton.usf().distance_centimeters < 10):
        Kleiton.steering_pair().on(0, -15)
        sleep(0.3)

    else:
        Kleiton.steering_pair().off()
    
    Kleiton.girar_pro_lado("dir",90)

def realinhar(Kleiton):
    while(distancia_min(Kleiton.usl()) > 30):
        Kleiton.steering_pair().on_for_degrees(0, -15, 32*(2))

    else :
        Kleiton.steering_pair().on_for_degrees(0, -15, 32*(4))

    while(distancia_min(Kleiton.usl()) < 20):
        Kleiton.steering_pair().on(0, 10)

    else:
        Kleiton.steering_pair().off()
    
    while(distancia_min(Kleiton.usl()) > 20):
        Kleiton.steering_pair().on(0, -10)

    else :
        Kleiton.steering_pair().off()

def baliza(Kleiton):
    distancia = 32*distancia_min(Kleiton.usl())

    if(distancia > dist_maxima):
        logger.warning('Distância baliza maior que a distância máxima\n Distância = {}'.format(distancia))
    else:
        logger.debug('Distância baliza = {}'.format(distancia))

    Kleiton.steering_pair().on_for_degrees(0,15,100)

    Kleiton.girar_pro_lado("esq",75)
    sleep(0.5)

    Kleiton.steering_pair().on_for_degrees(0, -15, distancia)
    sleep(0.5)
    
    Kleiton.girar_pro_lado("dir",75)
    sleep(0.5)

    Kleiton.steering_pair().on_for_degrees(0, 10, 32*(7))
    sleep(0.5)
            
def pegar(Kleiton):
    Kleiton.garra_g().on_for_seconds(100, 2)
    sleep(0.5)
    Kleiton.garra_m().on_for_degrees(60, -400)
    sleep(0.5)
    Kleiton.garra_g().on_for_degrees(40, -1150 )

def pegar_cano(Kleiton):    
    reposicionar_garra(Kleiton)
    achar_cano(Kleiton)
    alinhar_com_cano(Kleiton)
    empurrar_cano(Kleiton)
    realinhar(Kleiton)
    baliza(Kleiton)
    pegar(Kleiton)

if __name__ == '__main__':
    Kleit = Robot()
    pegar_cano(Kleit)
