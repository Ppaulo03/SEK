#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor, ColorSensor, UltrasonicSensor
from time import sleep
import os.path

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

def acharborda():
    while cor_dir.color==cor_esq.color:
        steering_pair.on(0,10)
    else:
        steering_pair.off()
    return

def girando_na_borda(angulo, lado): #1 esq, -1 dir
    rot = angulo*4
    steering_pair.on_for_degrees(lado*51,-10, rot)
    return

h = os.path.exists("cores.txt")

def autocompletar(cor1, cor2):
    A = {cor1, cor2}
    B = {2,4,5}
    cor = max(B - A)
    return cor 

if h==False:                            #verificar se já existe o arquivo, se não existir:
    cores = open("cores.txt", "w+")     #cria o arquivo 
    cores.close()                       #fecha o arquivo
    girando_na_borda(90,1)              #90 graus pra esquerda
    acharborda()                        #acha a linha preta e se alinha
    steering_pair.on_for_degrees(0,-10,25)
    alinhamento()
    sleep(1)
    steering_pair.on_for_degrees(0,10,25)
    sleep(1)
    acharborda()                       #acha a primeira cor e se alinha
    alinhamento()
    sleep(1)
    steering_pair.on_for_degrees(0,10,360)
    cor1 = cor_esq.color                #salvar primeira cor
    cores = open("cores.txt", "a")
    cores.write(str(cor1))
    cores.close()
    sleep(7)
    steering_pair.on_for_degrees(0,10,100)
    girando_na_borda(90,1)              #90 graus pra esquerda
    acharborda()                        #achar segunda cor
    steering_pair.on_for_degrees(0,-10,25)
    alinhamento()
    steering_pair.on_for_degrees(0,10,200)
    cor2 = cor_esq.color                #salvar segunda cor
    cores = open("cores.txt", "a")
    cores.write(str(cor2))
    cores.close()
    cor3 = autocompletar(cor1, cor2)    #autocompletar 3a cor
    cores = open("cores.txt", "a")
    cores.write(str(cor3))
    cores.close()

steering_pair.on_for_degrees(100,20,180)