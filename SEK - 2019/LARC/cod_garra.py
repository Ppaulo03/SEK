#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MediumMotor, MoveSteering, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from time import sleep
import math

ent_motor_medio = OUTPUT_A
ent_motor_grande = OUTPUT_B
ent_motor_esq = OUTPUT_C
ent_motor_dir = OUTPUT_D

ent_us_fr = INPUT_1
ent_us_lat = INPUT_2
ent_sc_esq = INPUT_3
ent_sc_dir = INPUT_4

steering_pair = MoveSteering(ent_motor_esq, ent_motor_dir)

elevador_g = LargeMotor(ent_motor_grande)
garra_m = MediumMotor(ent_motor_medio)

# elevador_g.on_for_degrees(40, -180) # negativo sobe
# garra_m.on_for_degrees(40, 96)  # positivo abre

cor_esq = ColorSensor(ent_sc_esq)
cor_dir = ColorSensor(ent_sc_dir)
us_lat = UltrasonicSensor(ent_us_lat)
us_front = UltrasonicSensor(ent_us_fr)

sound = Sound()
btn = Button()

tam_cano = 0

# começar código
# sound.beep()

def cor_tamanho_cano():
    if cor_esq or cor_dir == 'azul':
        tam_cano = 5
    elif cor_esq or cor_dir == 'vermelho':
        tam_cano = 2.5
    elif cor_esq or cor_dir == 'amarelo':
        tam_cano = 1
    
    return tam_cano

def distancia_min(sensor):
    a1 = sensor.distance_centimeters
    sleep(0.05)

    a2 = sensor.distance_centimeters
    sleep(0.05)

    a3 = sensor.distance_centimeters
    sleep(0.05)

    a4 = sensor.distance_centimeters
    sleep(0.05)

    a5 = sensor.distance_centimeters
    sleep(0.05)

    a6 = sensor.distance_centimeters
    sleep(0.05)

    a7 = sensor.distance_centimeters
    sleep(0.05)

    a8 = sensor.distance_centimeters
    sleep(0.05)

    a9 = sensor.distance_centimeters
    sleep(0.05)

    a10 = sensor.distance_centimeters
    sleep(0.05)

    distancia = min(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10)

    return distancia

#p cano 20 cm o robo tem q andar 23cm pra garra conseguir pegar
#p cano 15 o robo tem q andar 18cm pra conseguir pegar
#p cano de 10 o robo tem q andar 17 cm

def pega_cano2():
    elevador_g.on_for_seconds(100, 2)
    sleep(1)

    garra_m.on_for_degrees(60, 200)

    elevador_g.on_for_degrees(40, 32*(-10))
    sleep(3)

    dist_maxima = 45
    while (distancia_min(us_lat) > dist_maxima): 
        steering_pair.on(0, 20) # robo sai procurando por canos.

        #funcao alinha
    else:
        steering_pair.off() # para pq achou o cano
        sleep(1)

        distancia_1 = us_lat.distance_centimeters
        
        steering_pair.on_for_degrees(100, 20, 2.2*(-90)) # gira para esquerda (frontal de frente p cano)
        sleep(1)

        steering_pair.on_for_degrees(0, 15, 32*(distancia_1/2))
        sleep(1)

        steering_pair.on_for_degrees(100, 20, 2.2*(90)) # gira de voltA (lateral de frente p cano)

    while (distancia_min(us_lat) > dist_maxima - distancia_1/2): # anda ate chegar no comeco do cano
        steering_pair.on(0, 20)
    else:
        steering_pair.off()

    while (distancia_min(us_lat) < dist_maxima - distancia_1/2): #andar ate chegar ao final do cano
        steering_pair.on(0, 20)
    else:
        steering_pair.off() 
        steering_pair.on_for_degrees(0, -15, 32*(6)) #da uma re pra concertar o erro

    steering_pair.on_for_degrees(100, 20, 2.2*(-90)) # gira para esquerda (frontal de frente p cano)

    while(us_front.distance_centimeters > 7):
        steering_pair.on(0, 15) #empurra o cano
        sleep(0.3)
    else:
        steering_pair.off()
        steering_pair.on_for_seconds(0,20, 1) 
        sleep(0.5)
    
    while(us_front.distance_centimeters < 10):
        steering_pair.on(0, -15) #da re
        sleep(0.3)
    else:
        steering_pair.off()
        #corrige primeiro giro
        steering_pair.on_for_degrees(100, 20, 2.2*(90)) # gira para direita (lateral de frente p cano

    while(distancia_min(us_lat) > 30):
        steering_pair.on_for_degrees(0, -15, 32*(2)) # da re ate ver o cano
    else :
        steering_pair.on_for_degrees(0, -15, 32*(4))
        x = distancia_min(us_lat) #x é da distancia do sensor ao cano antes da baliza
        y = 10*32*x/10 #angulo da baliza

    while(distancia_min(us_lat) < 20):
        steering_pair.on(0, 10)
    else:
        steering_pair.off() #para pq n ve mais o cano
    
    while(distancia_min(us_lat) > 20):
        steering_pair.on(0, -10)
    else :
        steering_pair.off()

#baliza
    #chega pra frente
    steering_pair.on_for_degrees(0,15,100)

    #gira p direita
    steering_pair.on_for_degrees(50, 15, 2.43*75)
    sleep(0.5)

    #ré na diagonal
    steering_pair.on_for_degrees(0, -15, y)
    sleep(0.5)
    
    # gira dnvo o contrario do 1 giro 
    steering_pair.on_for_degrees(50, 15, 2.43*-75)

    sleep(0.5)

    steering_pair.on_for_degrees(0, 10, 32*(7)) #anda a quantidade que o robo tem q voltar pra pegar o cano - variavel
    sleep(0.5)
            
    elevador_g.on_for_seconds(100, 2)  # desce positivo
    sleep(0.5)
            
    garra_m.on_for_degrees(60, -400) # fechar garra
    sleep(0.5)
            
    elevador_g.on_for_degrees(40, -1150 )  # sobe negativo


pega_cano2()

def colocar_cano():
    # dist sensor -> gasoduto = 10cm
    garra_m.on_for_degrees(60, -200) # fecha garra
    garra_m.stop_action = 'hold'
    elevador_g.on_for_degrees(40, -820)  # negativo sobe
    elevador_g.stop_action = 'hold'

    #chega pra frente
    steering_pair.on_for_degrees(0,15, 100)

    #gira p direita
    steering_pair.on_for_degrees(50, 15, 2.43*75)

    sleep(3)

    #ré na diagonal
    steering_pair.on_for_degrees(0, -15, 13*32)
 
    sleep(3)
 
    # gira dnvo o contrario do 1 giro 
    steering_pair.on_for_degrees(100, 15, 2.43*-65/2)
 
    sleep(3)
 
    #chega um pouco pra frente(conserta)
    steering_pair.on_for_degrees(-15, 15, 2.43*30)
    sleep(3)

    #elevador desce um pouco
    elevador_g.on_for_degrees(40, 180)  # pos desce
    sleep(3)

    #abre garra
    garra_m.on_for_degrees(10, 300)
    sleep(1)

    # gira pra frente
    steering_pair.on_for_degrees(100, 15, 2.43*65/2)
    sleep(1)

    #re invertida (vai pra frentne)
    steering_pair.on_for_degrees(0, -15, 13*-32)
    sleep(1)

    #gira pra esquerda
    steering_pair.on_for_degrees(50, 15, 2.43*-75)
    sleep(1),


