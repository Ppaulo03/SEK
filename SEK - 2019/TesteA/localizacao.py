#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor, ColorSensor, UltrasonicSensor
from time import sleep

#1 direita, -1 esquerda
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
vazio = 3

def alinhamento(): #função testada e aprovada!
    cor_esq_inicial = cor_esq.color
    cor_dir_inicial = cor_dir.color
    for j in range(0,4):
        while cor_esq.color==cor_dir.color and cor_esq.color==cor_dir_inicial:#andar até um dos sensores mudar
            steering_pair.on(0,10)
        else:
            steering_pair.off()
            steering_pair.on_for_degrees(0,-10,15) #correção da posição do sensor
            steering_pair.off()

        if cor_esq.color!=cor_esq_inicial:#vamos ver qual lado mudou
            lado = -1
            borda = cor_esq.color
        else:
            lado = 1
            borda = cor_dir.color

        while cor_esq.color==cor_dir_inicial and cor_dir.color==cor_dir_inicial: #enquanto os sensores estiverem sobre suas cores iniciais, o robô gira
            steering_pair.on(lado*60, 10) #50 faz com que uma das rodas esteja parada, mas isso desloca o sensor
        else:
            steering_pair.off()
            sleep(1)

    return

def girando_na_borda(angulo, lado): #1 direita, -1 esquerda
    rotacoes=1.1*angulo/90
    steering_pair.on_for_rotations(lado*55,-10,rotacoes)
    return
#as rotações variam com o atrito das rodas traseiras
 
def testar_vazio():
    girando_na_borda(90, 1) #girar pra direita 90 graus
    while cor_esq.color==6 and cor_dir.color==6:
        steering_pair.on(0,30)
    else:
        steering_pair.off()
        if cor_dir.color==1 or cor_dir.color==1:
            vazio = 1 #vazio errado
        else:
            vazio = 0 #vazio certo
    return

#aqui começa o código

alinhamento()