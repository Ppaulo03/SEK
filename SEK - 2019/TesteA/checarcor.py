#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor, ColorSensor, UltrasonicSensor
from ev3dev2.sound import Sound
from time import sleep
import os.path

sound = Sound()
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

check = open("check.txt", "w+")     #cria o arquivo 
check.write('**Teste**')
check.close()
sound.beep()
sleep(5)
def salvar(*args):
    for arg in args:
        e = cor_esq.raw
        d = cor_dir.raw
        eh = cor_esq.hsv
        dh = cor_dir.hsv
        a = '\nRGB esquerdo: ' + str(e) + '  RGB direito: ' + str(d) + '\n'
        b = 'HSV esquerdo: ' + str(eh) + '  HSV direito: ' + str(dh) + '\n\n'
        c = arg + a + b
        check = open("check.txt", "a") 
        check.write(c)
        check.close()
        sound.beep()
        sleep(5)

salvar('branco','preto','azul','vermelho','amarelo','verde','vazio')