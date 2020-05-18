#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MediumMotor, MoveSteering, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from time import sleep
#import os.path

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

# começar código
# sound.beep()

# waiting = True

# while waiting:
#     if btn.any():    # Checks if any button is pressed.
#         sound.beep()  # Wait for the beep to finish.
#         waiting = False
#     else:
#         sleep(0.01)  # Wait 0.01 second

# us frontal identifica o cano


def pegar_cano():
    while us_front.distance_centimeters >= 8:
        steering_pair.on_for_degrees(0, 10, 90)

    else:
        # gira 90º para direita. No cod 03 existe a func girar p lado
        steering_pair.on_for_degrees(60, 10, 360)
        garra_m.on_for_degrees(60, -160)  # negativo fecha
        elevador_g.on_for_degrees(40, -820)  # negativo sobe

def baliza():
    garra_m.on_for_degrees(60, -200)
    garra_m.stop_action = 'hold'
    elevador_g.on_for_degrees(40, -820)  # negativo sobe
    elevador_g.stop_action = 'hold'

    # #chega pra frente
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
    sleep(1)
    
baliza()


def colocar_cano():
    

    # O robo deve ficar numa distancia de +- 15 cm
    # bloco de prog pra alinha ao gasoduto(...)

    while 14 < us_lat.distance_centimeters < 30:  # dist do ultrassonico ao 'cano'
        steering_pair.on_for_degrees(0, 30, 90) #existe cano no gasoduto, continua reto
        sound.beep()
    else:
        elevador_g.on_for_degrees(60, 800) # desce o elevador para verificar se existe um gasoduto
        if(us_lat.distance_centimeters < 20):
            #cod para medir o tamanho gasoduto(rafa)
            #voltar o que foi percorrido
            steering_pair.on_for_degrees(-60,10,60) #vira pra esquerda pra aproximar do gasoduto

        else:
            steering_pair.on_for_degrees(0, 30, 90) #cod para andar reto

# tank_deviec = MoveTank(OUTPUT_C, OUTPUT_D)
# tank_deviec.follow_line



# pegar_cano()
# colocar_cano()
