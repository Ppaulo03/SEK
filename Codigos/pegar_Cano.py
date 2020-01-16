#!/usr/bin/env python3
import math
import logging
from time import sleep
from time import time
import robo

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('/home/robot/Teste/Logs/pegar_cano.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(message)s'))
logger.addHandler(file_handler)

dist_maxima = 45

def distancia_min(sensor):
    cont=0
    distancia = []
    while(cont<10):
        distancia.append (sensor.distance_centimeters)
        sleep(0.05)
        cont+=1
    else:
        return min(distancia)
        
def reposicionar_garra():
    robo.garra_g.on_for_seconds(100, 2)
    sleep(1)
    robo.garra_m.on_for_degrees(60, 200)
    robo.garra_g.on_for_degrees(40, 32*(-10))
    sleep(3)

def achar_cano():
    while (distancia_min(robo.usl) > dist_maxima): 
        robo.steering_pair.on(0, 20)

    else:
        robo.steering_pair.off()
        sleep(1)

def alinhar_com_cano():
    distancia = robo.usl.distance_centimeters
    
    if(distancia > dist_maxima):
        logger.warning('Distância_1 maior que a distância máxima\n Distância = {}'.format(distancia))
    else:
        logger.debug('Distância_1 = {}'.format(distancia))
    
    robo.girar_pro_lado("esq",90)
    sleep(1)
    robo.steering_pair.on_for_degrees(0, 15, 32*(distancia/2))
    sleep(1)
    robo.girar_pro_lado("dir",90)
    while (distancia_min(robo.usl) > dist_maxima - (distancia/2)):
        robo.steering_pair.on(0, 20)

    else:
        robo.steering_pair.off()

    while (distancia_min(robo.usl) < dist_maxima - distancia/2):
                robo.steering_pair.on(0, 20)

    else:
        robo.steering_pair.off() 
        robo.steering_pair.on_for_degrees(0, -15, 32*(6))

def empurrar_cano():
    robo.girar_pro_lado("esq",90)

    if(robo.usf.distance_centimeters > dist_maxima):
        logger.warning('Distância frontal maior que a distância máxima\n Distância = {}'.format(robo.usf.distance_centimeters))
    else:
        logger.debug('Distância frontal = {}'.format(robo.usf.distance_centimeters))

    while(robo.usf.distance_centimeters > 7):
        robo.steering_pair.on(0, 15)
        sleep(0.3)

    else:
        robo.steering_pair.off()
        robo.steering_pair.on_for_seconds(0,20, 1) 
        sleep(0.5)
    
    while(robo.usf.distance_centimeters < 10):
        robo.steering_pair.on(0, -15)
        sleep(0.3)

    else:
        robo.steering_pair.off()
    
    robo.girar_pro_lado("dir",90)

def realinhar():
    while(distancia_min(robo.usl) > 30):
        robo.steering_pair.on_for_degrees(0, -15, 32*(2))

    else :
        robo.steering_pair.on_for_degrees(0, -15, 32*(4))

    while(distancia_min(robo.usl) < 20):
        robo.steering_pair.on(0, 10)

    else:
        robo.steering_pair.off()
    
    while(distancia_min(robo.usl) > 20):
        robo.steering_pair.on(0, -10)

    else :
        robo.steering_pair.off()

def baliza():
    distancia = 32*distancia_min(robo.usl)

    if(distancia > dist_maxima):
        logger.warning('Distância baliza maior que a distância máxima\n Distância = {}'.format(distancia))
    else:
        logger.debug('Distância baliza = {}'.format(distancia))

    robo.steering_pair.on_for_degrees(0,15,100)

    robo.girar_pro_lado("esq",75)
    sleep(0.5)

    robo.steering_pair.on_for_degrees(0, -15, distancia)
    sleep(0.5)
    
    robo.girar_pro_lado("dir",75)
    sleep(0.5)

    robo.steering_pair.on_for_degrees(0, 10, 32*(7))
    sleep(0.5)
            
def pegar():
    robo.garra_g.on_for_seconds(100, 2)
    sleep(0.5)
    robo.garra_m.on_for_degrees(60, -400)
    sleep(0.5)
    robo.garra_g.on_for_degrees(40, -1150 )

def pegar_cano():    
    reposicionar_garra()
    achar_cano()
    alinhar_com_cano()
    empurrar_cano()
    realinhar()
    baliza()
    pegar()

if __name__ == '__main__':
    pegar_cano()
