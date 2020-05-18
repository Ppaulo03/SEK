#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MediumMotor, MoveSteering, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor , UltrasonicSensor
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from time import sleep
#import os.path

ent_motor_esq = OUTPUT_C
ent_motor_dir = OUTPUT_D
ent_motor_grande = OUTPUT_B
ent_motor_medio = OUTPUT_A
ent_sc_esq = INPUT_3
ent_sc_dir = INPUT_4
ent_us_lat = INPUT_2
ent_us_fr = INPUT_1
steering_pair = MoveSteering(ent_motor_esq, ent_motor_dir)
garra_g = LargeMotor(ent_motor_grande)
garra_m = MediumMotor(ent_motor_medio)
cor_esq = ColorSensor(ent_sc_esq)
cor_dir = ColorSensor(ent_sc_dir)
usl = UltrasonicSensor(ent_us_lat)
usf = UltrasonicSensor(ent_us_fr)
sound = Sound()
btn = Button()

#começar código
sound.beep()

waiting = True

while waiting:
    if btn.any():    # Checks if any button is pressed.
        sound.beep()  # Wait for the beep to finish.
        waiting = False
    else:
        sleep(0.01)  # Wait 0.01 second

gasoduto_com_cano = True

# while com_cano:
#     garra_g.on_for_degrees(20,-1300)
#     sleep(0.1)
#     com_cano = (usl.distance_centimeters < 15)
#     sleep(0.01)
#     garra_g.on_for_degrees(20,1300)
#     sleep(0.01)

# while com_cano and (usl.distance_centimeters < 12 and not(garra_g.is_running)):
#     steering_pair.on_for_degrees(0,10,200)
#     garra_g.on_for_degrees(20,-1350)
#     sleep(0.1)
#     com_cano = (usl.distance_centimeters < 30)
#     if com_cano:
#         sound.beep()
#     sleep(0.01)
#     garra_g.on_for_degrees(20,1350)
#     sleep(0.01)
# else:
#     steering_pair.off()


def girar_pro_lado(lado,angulo):
    if lado == 'esq':
        steering_pair.on_for_degrees(-60,10,angulo*3.5)
    elif lado == 'dir':
        steering_pair.on_for_degrees(60,10,angulo*3.5)

no_gasoduto = True

while no_gasoduto:
    while gasoduto_com_cano and usl.distance_centimeters < 15 and usf.distance_centimeters > 10:
        #dist = usl.distance_centimeters
        for i in range (3):
            steering_pair.on_for_degrees(0,10,100)
            sleep(0.01)
        # dist1 = dist
        # dist = usl.distance_centimeters
        # if dist1 > dist:
        #     steering_pair(-10,) (fazer um esquema que a diferença da leitura já dá o steering do proximo passo)
            if usl.distance_centimeters > 15 or usf.distance_centimeters < 10:
                break
        if gasoduto_com_cano and usl.distance_centimeters < 15 and usf.distance_centimeters > 10:
            garra_g.on_for_degrees(20,-1250)
            sleep(0.1)
            gasoduto_com_cano = (usl.distance_centimeters < 30)
            if gasoduto_com_cano:
                sound.speak('ok')
            sleep(0.01)
            garra_g.on_for_degrees(20,1250)
            sleep(0.01)
    while gasoduto_com_cano and usf.distance_centimeters < 10:
        girar_pro_lado('dir',90)
        sleep(3)
    while gasoduto_com_cano and usl.distance_centimeters > 15 and usf.distance_centimeters > 10:
        girar_pro_lado('esq',90)
        sleep(3)
    while not(gasoduto_com_cano):
        steering_pair.on_for_degrees(0,-10,100)
        break
    #no_gasoduto = gasoduto_com_cano #alterar ou colocar no while not(g...) uma maneira de colocar gasoduto_com_cano = True no final 
    buscar_novo_cano = not(no_gasoduto)
    meeting_area = not(buscar_novo_cano)