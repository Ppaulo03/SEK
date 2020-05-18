#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MediumMotor, MoveSteering, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor , UltrasonicSensor
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from time import sleep
import math
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

def RGBtoHSV(rgb):
    x = max(rgb)
    y = min(rgb)
    if x==y:
        z = 1
    else:
        z = x-y
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    if r>=g and r>=b: #se o vermelho é o máximo
        if g>=b:
            h = 60*(g-b)/z
        else:
            h = 360 + (60*(g-b)/z)
    elif g>=r and g>=b: # se verde é o máximo
        h = 120 + (60*(b-r)/z)
    else:
        h = 240 + (60*(r-g)/z)
    s = z/(x+1)
    v = x/255
    hsv_lido = [h,s,v]
    return hsv_lido

def escalarRGB(rgb_in,rgb_max):
    rcor = 255.0*rgb_in[0]/rgb_max[0]
    gcor = 255.0*rgb_in[1]/rgb_max[1]
    bcor = 255.0*rgb_in[2]/rgb_max[2]
    rgb_cor = [rcor,gcor,bcor]
    for i in range(0,3):
        if rgb_cor[i] > 255:
            rgb_cor[i] = 255
        if rgb_cor[i] < 0:
            rgb_cor[i] = 0
    return rgb_cor

def definir_rgbmax(snr):
    if snr=='esq':
        sensor=cor_esq
    else:
        sensor=cor_dir
    rgbmax = [sensor.red,sensor.green,sensor.blue]
    return rgbmax

def cor(sensor):        #atualizada 13/set
    if sensor=='esq':       #definir as referências
        snr = cor_esq
        rgb_max = rgbmax_e  #chamar definir_rgbmax(snr) antes
        s_max_branco = 0.05000
        v_min_branco = 0.70000
        v_max_preto = 0.15000
        v_min_preto = 0.05000
        vermelho = (5,0.8612,0.8196)    #rve: componente (H)ue da referencia do (V)ermelho do sensor (E)squerdo
        azul = (220.0,70.0,50.0)
        amarelo = (40.0,0.8588,0.998)
        verde = (170.0,0.8909,0.4314)
    if sensor=='dir':
        snr = cor_dir
        rgb_max = rgbmax_d
        s_max_branco = 0.05000
        v_min_branco = 0.70000
        v_max_preto = 0.15000
        v_min_preto = 0.05000
        vermelho = (5.0,0.8612,0.8196)    #rve: componente (H)ue da referencia do (V)ermelho do sensor (E)squerdo
        azul = (220.0,70,50)
        amarelo = (40.0,0.8588,0.998)
        verde = (170.0,0.8909,0.4314)
    rgb_cru = [snr.red,snr.green,snr.blue] #colocar na lista as componentes
    rgb = escalarRGB(rgb_cru,rgb_max)               #escalo pra 255
    hsv = RGBtoHSV(rgb)                             #converte pra hsv
    if hsv[2] > v_min_branco and hsv[1] < s_max_branco:
        return 'branco'
    elif hsv[2] < v_max_preto and hsv[2] > v_min_preto:
        return 'preto'
    elif hsv[2] < 0.01:                #se o v está muito baixo, estamos no vazio
        return 'vazio'
    elif (hsv[0] > (azul[0]-15)) and (hsv[0] < (azul[0]+15)):  
        return 'azul'
    elif (hsv[0] < (vermelho[0]+15)) or (hsv[0] > (vermelho[0]+345)):
        return 'vermelho'
    elif (hsv[0] > (amarelo[0]-15)) and (hsv[0] < (amarelo[0]+15)):
        return 'amarelo'
    elif (hsv[0] > (verde[0]-15)) and (hsv[0] < (verde[0]+15)):
        return 'verde'
    else:
        return 'semcor'

def alinhamento(): #alinhamento 2.0 13/set
    cor_esq_inicial = cor('esq')
    cor_dir_inicial = cor('dir')
    while cor_dir_inicial==cor('dir') and cor('esq')==cor_esq_inicial:
        steering_pair.on(0,10)
    else:
        steering_pair.off()
        sleep(0.01)
    cor_aux_e = cor('esq')
    cor_aux_d = cor('dir')
    if cor('esq')==cor('dir'):
        steering_pair.off()
    elif cor_dir_inicial!=cor_aux_d:
        #lado=1
        while cor('esq')==cor_aux_e:
            steering_pair.on(60,10)
        else:
            steering_pair.off()
        steering_pair.on_for_degrees(0,10,10)
    else:
        #lado=-1
        while cor('dir')==cor_aux_d:
            steering_pair.on(-60,10)
        else:
            steering_pair.off()
        steering_pair.on_for_degrees(0,10,10)
    sleep(0.01)
    return

def girar_pro_lado(lado,angulo):
    if lado == 'esq':
        steering_pair.on_for_degrees(-60,10,angulo*3.5)
    elif lado == 'dir':
        steering_pair.on_for_degrees(60,10,angulo*3.5)

#começar código
sound.beep()
rgbmax_e = definir_rgbmax('esq')
rgbmax_d = definir_rgbmax('dir')

waiting = True

while waiting:
    if btn.any():    # Checks if any button is pressed.
        sound.beep()  # Wait for the beep to finish.
        waiting = False
    else:
        sleep(0.01)  # Wait 0.01 second

meeting_area = True
no_preto = False
antes_preto = False
no_vazio = False
aprender_cores = False

while meeting_area:
    alinhamento()
    no_vazio = (cor('esq')=='vazio' or cor('esq')=='semcor') and (cor('dir')=='vazio' or cor('dir')=='semcor')
    no_preto = (cor('esq')=='preto' or cor('dir')=='preto')
    if no_preto:
        steering_pair.on_for_degrees(0,-10,300)
        girar_pro_lado('dir',90)
        antes_preto = True
    else:
        if (cor('esq')=='verde' or cor('dir')=='verde'):
            steering_pair.on_for_degrees(0,-10,300)
            girar_pro_lado('dir',180)
        elif (no_vazio and not(antes_preto)):
            steering_pair.on_for_degrees(0,-10,300)
            girar_pro_lado('dir',90)    
    meeting_area = not(no_vazio and antes_preto)
    aprender_cores = (not meeting_area)
sound.speak('congratulations')
