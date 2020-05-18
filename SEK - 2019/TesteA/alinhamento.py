#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor, ColorSensor, UltrasonicSensor
from time import sleep

ent_motor_esq = OUTPUT_A
ent_motor_dir = OUTPUT_B
ent_sc_esq = INPUT_1
ent_sc_dir = INPUT_2
#ent_us_lat = INPUT_3
#ent_us_fr = INPUT_4
steering_pair = MoveSteering(ent_motor_esq, ent_motor_dir)
cor_esq = ColorSensor(ent_sc_esq)
cor_dir = ColorSensor(ent_sc_dir)
#us_lat = UltrasonicSensor(ent_us_lat)
#us_fr = UltrasonicSensor(ent_us_fr)
lado_manobra = 0
vazio = 3

def alinhamento(): #alinhamento 1.0
    cor_esq_inicial = cor_esq.color
    cor_dir_inicial = cor_dir.color
    while cor_dir_inicial==cor_dir.color and cor_esq.color==cor_esq_inicial:
        steering_pair.on(0,10)
    else:
        steering_pair.off()
        sleep(0.5)
        cor_aux_e = cor_esq.color
        cor_aux_d = cor_dir.color
        if cor_dir_inicial!=cor_aux_d:
            lado=1
            while cor_esq.color==cor_aux_e:
                steering_pair.on(60,10)
            else:
                steering_pair.off()
        else:
            lado=-1
            while cor_dir.color==cor_aux_d:
                steering_pair.on(-60,10)
            else:
                steering_pair.off()
    sleep(0.5)
    return

alinhamento()
