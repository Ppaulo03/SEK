#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_A, OUTPUT_B # , OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2 #INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor# , UltrasonicSensor
from time import sleep
from ev3dev2.sound import Sound
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
sound = Sound()

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

def cor(sensor):
    if sensor=='esq':       #definir as referências
        snr = cor_esq
        rgb_max = rgbmax_e
        s_max_branco = 0.095794                             #0.065794;
        v_min_branco = 0.623137                             #0.793137
        v_max_preto = 0.179412
        v_min_preto = 0.059275                              #0.08
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
    if hsv[2] > v_min_branco:       #se o v do hsv lido é maior que o v mínimo pro branco
        if hsv[1] < s_max_branco:
            cor = 'branco'
            return cor
    elif hsv[2] < v_max_preto:      #preto tb só verifica o v
         if hsv[2] > v_min_preto:
             cor = 'preto'
             return cor
    elif hsv[2] < 0.01:                #se o v está muito baixo, estamos no vazio
         cor = 'vazio'
         return cor 
    elif (hsv[0] > (azul[0]-15)) and (hsv[0] < (azul[0]+15)):           #se o h do azul tá no range
         cor = 'azul'
         return cor 
    elif (hsv[0] < (vermelho[0]+15)) and (hsv[0] > (vermelho[0]+345)):  #se o h do vermelho tá no range
         cor = 'vermelho'
         return cor 
    elif (hsv[0] > (amarelo[0]-15)) and (hsv[0] < (amarelo[0]+15)):     #se o h do amarelo tá no range
         cor = 'amarelo'
         return cor 
    elif (hsv[0] > (verde[0]-15)) and (hsv[0] < (verde[0]+15)):         #se o h do verde tá no range
         cor = 'verde'
         return cor 
    else:
        cor = 'semcor'
        return cor

rgbmax_e = definir_rgbmax('esq')
rgbmax_d = definir_rgbmax('dir')

ce = cor('esq')
cd = cor('dir')

sound.beep()
sleep(1)
if ce==cd:
    steering_pair.on_for_seconds(0,10,2)
    sound.speak('arrived')
sleep(7)

sound.beep()
sleep(1)
while cor('esq')==cor('dir'):
    steering_pair.on(0,10)
else:
    steering_pair.off()
    sound.speak('stop')
sleep(7)

sound.beep()
sleep(1)
while cor('esq')=='branco':
    steering_pair.on(0,10)
else:
    steering_pair.off()
    sound.speak('stop')
sleep(7)

sound.beep()
sleep(1)
while cor('dir')=='branco':
    steering_pair.on(0,10)
else:
    steering_pair.off()
    sound.speak('stop')
sleep(3)