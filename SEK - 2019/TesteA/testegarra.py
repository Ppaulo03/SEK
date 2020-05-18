#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
#from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
#from ev3dev2.sensor.lego import ColorSensor , UltrasonicSensor
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from time import sleep
#import math
#import os.path

#   DEFINIÇÕES

# ent_motor_esq = OUTPUT_C
# ent_motor_dir = OUTPUT_D
ent_motor_grande = OUTPUT_B
ent_motor_medio = OUTPUT_A

#
# steering_pair = MoveSteering(ent_motor_esq, ent_motor_dir)
garra_g = LargeMotor(ent_motor_grande)
garra_m = MediumMotor(ent_motor_medio)

sound = Sound()
btn = Button()

waiting = True

while waiting:
    if btn.any():    # Checks if any button is pressed.
        sound.beep()  # Wait for the beep to finish.
        global waiting
        waiting = False
    else:
        sleep(0.01)  # Wait 0.01 second

garra_m.on_for_degrees(60,-200)
garra_g.on_for_degrees(20,-1100)