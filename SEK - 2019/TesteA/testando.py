#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor, ColorSensor, UltrasonicSensor
from time import sleep
from ev3dev2.sound import Sound

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
sound = Sound()
i=0
bordas = open("alinhamento.txt", "w+")     #cria o arquivo 
bordas.write('**Alinhamento**')
bordas.close()
cor_dir.calibrate_white()
cor_esq.calibrate_white()

while i<6:
    alinhamento()
    a = '\nE: ' + str(cor_esq.color_name) + '   D: ' + str(cor_dir.color_name)
    bordas = open("alinhamento.txt", "a")
    bordas.write(a)
    bordas.close()
    sound.beep()
    i += 1
    sleep(5)

sound.beep()
sound.beep()




#próximo teste


def acharborda():
    #0: vazio, 1:preto, 2:azul, 3:verde, 4:amarelo, 5:vermelho, 6:branco
    while cor_dir.color!=cor_esq.color:
        steering_pair.on(0,-10)
    else:
        steering_pair.off()    
    steering_pair.on_for_degrees(0,-10,35)
    cor_inicial_d = cor_dir.color
    cor_inicial_e = cor_esq.color
    while cor_dir.color==cor_inicial_d and cor_esq.color==cor_inicial_e:
        steering_pair.on(0,10)
    else:
        steering_pair.off()
    if cor_dir.color!=cor_inicial_d:
        cor_borda = cor_dir.color
        sensor = 'd'
    else:
        cor_borda = cor_esq.color
        sensor = 'e'
    saida = '\nE: ' + str(cor_inicial_e) + '   D: ' + str(cor_inicial_d) + '\nBorda: ' +str(cor_borda)+sensor + '\nE: ' + str(cor_esq.green) + '   D:' + str(cor_dir.green)
    return saida

sleep(5)

bordas = open("bordas.txt", "w+")     #cria o arquivo 
bordas.close()                       #fecha o arquivo
sound.beep()
sleep(3)

cor_dir.calibrate_white()
cor_esq.calibrate_white()

i=0
while i<6:
    a = acharborda()
    bordas = open('bordas.txt','a')
    bordas.write(a)
    bordas.close()
    i = i+1
    sound.beep()
    sleep(5)
