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
score=0
cor_vista = 0



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
        #lado=1
        while cor_esq.color==cor_aux_e:
            steering_pair.on(60,10)
        else:
            steering_pair.off()
    else:
        #lado=-1
        while cor_dir.color==cor_aux_d:
            steering_pair.on(-60,10)
        else:
            steering_pair.off()
    sleep(0.5)
    return


def girando_na_borda(angulo, lado): #1 esq, -1 dir
    rot = angulo*4
    steering_pair.on_for_degrees(lado*51,-10, rot)
    return

def qual_cor(sensor):
    cores = {'e':[27,199,114],
             'd':[23,150,64]}
    re = cor_esq.red
    rd = cor_dir.red
    ge = cor_esq.green
    gd = cor_dir.green
    be = cor_esq.blue
    bd = cor_dir.blue
    ne = [re,ge,be]
    nd = [rd,gd,bd]
    i = 0
    score = 0
    cor_vista = 0
    if sensor=='d':
        n=nd
    else:
        n=ne
    cor_vista = 0
    while i < 3:
        v = n[i]
        li = cores[sensor][i] - 20
        ls = cores[sensor][i] + 20
        if li <= v <= ls:
            score += 1
        i = i+1
        if score >=2:
            cor_vista = 3
    return cor_vista

def acharborda():
    while cor_dir.color==cor_esq.color:
        steering_pair.on(0,10)
    else:
        steering_pair.off()
    return

def acharbordaverde():
    ctrl = 0
    while ctrl == 0:
        while cor_dir.color==cor_esq.color:
            steering_pair.on(0,10)
        else:
            steering_pair.off()
        if qual_cor('e')==3 or qual_cor('d')==3:
            steering_pair.on_for_degrees(-50,10,180)
        else:
            ctrl = 1
    return
#aqui começa o código

controle = 0
print('ok')
while controle==0:
    acharborda()                            #procura uma borda
    cor_vista = 0
    qe = qual_cor('d')
    qd = qual_cor('e')
    if qe==3 or qd==3:                      #verifica se ela é verde
        steering_pair.on_for_degrees(0,-10,200)
        steering_pair.on_for_degrees(-50,-10,180)
        acharborda()                               
    steering_pair.on_for_degrees(0,-10,45)  #volta pra se alinhar
    alinhamento()                           #se alinha
    sleep(0.5)
    if cor_dir.color==1 or cor_esq.color==1:    #faixa preta: virar pra direita
        girando_na_borda(100,-1)
#    elif qual_cor('e')==3 or qual_cor('d')==3:  #verde: rampa: virar pra esquerda
#        steering_pair.on_for_degrees(0,-10,45)
#        girando_na_borda(100,1)
    elif cor_dir.color==0 or cor_esq.color==0:  #não-cor: tem que descobrir se é o lado certo
        controle = 1

steering_pair.on_for_degrees(0,-10,100)
girando_na_borda(90,-1)                    #vira pra esquerda e repete o processo inicial
acharborda()
if cor_dir.color==1 or cor_esq.color==1:        #se achou a faixa: lado certo, volta
    steering_pair.on_for_degrees(0,-10,90)
    girando_na_borda(90,-1)
else:                                           #se achou a rampa: lado errado
    girando_na_borda(100,1)
    acharborda()
    steering_pair.on_for_degrees(0,-10,45)
    alinhamento()

