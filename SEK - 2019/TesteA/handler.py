#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_A, OUTPUT_B # , OUTPUT_C, OUTPUT_D
#from ev3dev2.sensor import INPUT_1, INPUT_2 #INPUT_3, INPUT_4
#from ev3dev2.sensor.lego import ColorSensor# , UltrasonicSensor
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from time import sleep
import os.path

ent_motor_esq = OUTPUT_A
ent_motor_dir = OUTPUT_B
#ent_sc_esq = INPUT_1
#ent_sc_dir = INPUT_2
#ent_us_lat = INPUT_3
#ent_us_fr = INPUT_4
steering_pair = MoveSteering(ent_motor_esq, ent_motor_dir)
#cor_esq = ColorSensor(ent_sc_esq)
#cor_dir = ColorSensor(ent_sc_dir)
#us_lat = UltrasonicSensor(ent_us_lat)
#us_fr = UltrasonicSensor(ent_us_fr)
sound = Sound()
btn = Button()

sound.beep()
sleep(3)
a = 1
b = 1
c = 1
while True:
    while a == 1 and b == 1:
        steering_pair.on_for_seconds(0,10,1)
        a = 0
        b = 1
        c = 0
        sleep(0.1)
    while a == 0 and b == 2:
        steering_pair.on_for_seconds(50,10,2)
        a = 0
        b = 0
        c = 0
        sleep(0.1)
    while b == 1 and c == 0:
        steering_pair.on_for_seconds(0,-10,1)
        a = 0
        b = 2
        sleep(0.1)
    if a == 0 and b == 0 and c == 0:
        steering_pair.off()
        sound.beep()
        sleep(1)
        exit()

#DEU CERTO CARALHO