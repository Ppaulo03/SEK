#!/usr/bin/env python3

from time import sleep
from time import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('/home/robot/Teste/Logs/robo.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(message)s'))
logger.addHandler(file_handler)

time_start = time()

import ev3dev2.motor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor , UltrasonicSensor
from ev3dev2.sound import Sound
from ev3dev2.button import Button

elapsed = time() - time_start
logger.info("Time for importations ev3: {}s".format(elapsed))
time_start = time()

ent_motor_esq = ev3dev2.motor.OUTPUT_C
ent_motor_dir = ev3dev2.motor.OUTPUT_D
ent_motor_grande = ev3dev2.motor.OUTPUT_B
ent_motor_medio = ev3dev2.motor.OUTPUT_A
ent_sc_esq = INPUT_3
ent_sc_dir = INPUT_4
ent_us_lat = INPUT_2
ent_us_fr = INPUT_1
mapadecores = ['amarelo','vermelho','azul']
tamanhos = ['vermelho','vermelho','amarelo','azul']
item_lista = 0

steering_pair = ev3dev2.motor.MoveSteering(ent_motor_esq, ent_motor_dir)
tank = ev3dev2.motor.MoveTank(ent_motor_esq,ent_motor_dir)
garra_g = ev3dev2.motor.LargeMotor(ent_motor_grande)
garra_m = ev3dev2.motor.MediumMotor(ent_motor_medio)
cor_esq = ColorSensor(ent_sc_esq)
cor_dir = ColorSensor(ent_sc_dir)
usl = UltrasonicSensor(ent_us_lat)
usf = UltrasonicSensor(ent_us_fr)
sound = Sound()
btn = Button()

rgbmax_dir = 0
rgbmax_esq = 0

elapsed = time() - time_start
logger.info("Time for declarations: {}s".format(elapsed))

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
    logger.debug('hsv_lido = {}'.format(hsv_lido))
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
    logger.debug('rgb_cor = {}'.format(rgb_cor))    
    return rgb_cor

def girar_pro_lado(lado,angulo):
    if lado == 'esq':
        steering_pair.on_for_degrees(-60,10,angulo*3.9)
    elif lado == 'dir':
        steering_pair.on_for_degrees(60,10,angulo*3.9)
    else:
        print("ERRO")

def definir_rgbmax(snr):
    if snr=='esq':
        sensor=cor_esq
    else:
        sensor=cor_dir
    rgbmax = [sensor.red,sensor.green,sensor.blue]
    logger.debug('rgbmax = {}'.format(rgbmax))
    return rgbmax
   
def cor(sensor):        
    s_max_branco = 0.05000
    v_min_branco = 0.70000
    v_max_preto = 0.3000
    v_min_preto = 0.09000
    v_max_vazio = 0.03
    vermelho = (5, 0.8612, 0.8196) 
    azul = (210.0, 70.0, 50.0)
    amarelo = (40.0, 0.8588, 0.998)
    if sensor=='esq':     
        snr = cor_esq
        rgb_max = rgbmax_esq
    if sensor=='dir':
        snr = cor_dir
        rgb_max = rgbmax_dir
    rgb_cru1 = [snr.red,snr.green,snr.blue]
    sleep(0.05)
    rgb_cru2 = [snr.red,snr.green,snr.blue]
    sleep(0.05)
    rgb_cru3 = [snr.red,snr.green,snr.blue]
    rgb_cru = [0,0,0]
    for i in range(3):
        rgb_cru[i]=(rgb_cru1[i]+rgb_cru2[i]+rgb_cru3[i])/3
    rgb = escalarRGB(rgb_cru,rgb_max)               
    hsv = RGBtoHSV(rgb)       
    logger.debug('rgbmax_dir = {}\nself.rgbmax_esq = {}'.format(rgbmax_dir,rgbmax_esq))                      
    if (rgb_cru[0]<9 and rgb_cru[1]<9 and rgb_cru[2]<9) or hsv[2]<v_max_vazio:
        return 'vazio'
    elif hsv[2] > v_min_branco and hsv[1] < s_max_branco:
        return 'branco'
    elif hsv[2] < v_max_preto and hsv[2] > v_min_preto:
        return 'preto'
    elif (hsv[0] > (azul[0]-15)) and (hsv[0] < (azul[0]+15)):  
        return 'azul'
    elif (hsv[0] < (vermelho[0]+15)) or (hsv[0] > (vermelho[0]+345)):
        return 'vermelho'
    elif (hsv[0] > (amarelo[0]-15)) and (hsv[0] < (amarelo[0]+15)):
        return 'amarelo'
    else:
        return 'semcor'

def testar_preto():
        steering_pair.on_for_degrees(0,10,150)
        if (cor('esq')!='azul' and cor('esq')!='vermelho' and cor('esq')!='amarelo'):
            steering_pair.on_for_degrees(0,-10,150)
            return False
        else:
            steering_pair.on_for_degrees(0,-10,150)
            return True

def alinhamento(): 
    cor_esq_inicial = cor('esq')
    cor_dir_inicial = cor('dir')
    while cor_dir_inicial==cor('dir') and cor('esq')==cor_esq_inicial:
        steering_pair.on(0,20)
    else:
        steering_pair.off()
        sleep(0.01)
    cor_aux_e = cor('esq')
    cor_aux_d = cor('dir')
    if cor('esq')==cor('dir'):
        steering_pair.off()
    elif cor_dir_inicial!=cor_aux_d:
        while cor('esq')==cor_aux_e:
            ev3dev2.motor.LargeMotor(ent_motor_esq).on(10)
        else:
            steering_pair.off()
        steering_pair.on_for_degrees(0,10,10)
    else:
        while cor('dir')==cor_aux_d:
            ev3dev2.motor.LargeMotor(ent_motor_dir).on(10)
        else:
            steering_pair.off()
        steering_pair.on_for_degrees(0,10,40)
    sleep(0.01)
    logger.debug('cor_dir = {}, cor_esq = {}'.format(cor('dir'),cor('esq')))

def alinhamento_pra_tras(): 
    cor_esq_inicial = cor('esq')
    cor_dir_inicial = cor('dir')
    while cor_dir_inicial==cor('dir') and cor('esq')==cor_esq_inicial:
        steering_pair.on(0,-15)
    else:
        steering_pair.off()
        sleep(0.01)
    cor_aux_e = cor('esq')
    cor_aux_d = cor('dir')
    if cor('esq')==cor('dir'):
        steering_pair.off()
    elif cor_dir_inicial!=cor_aux_d:
        while cor('esq')==cor_aux_e:
            ev3dev2.motor.LargeMotor(ent_motor_esq).on(-10)
        else:
            ev3dev2.motor.LargeMotor(ent_motor_esq).off()
        steering_pair.on_for_degrees(0,10,20)
    else:
        while cor('dir')==cor_aux_d:
            ev3dev2.motor.LargeMotor(ent_motor_dir).on(-10)
        else:
            ev3dev2.motor.LargeMotor(ent_motor_dir).off()
        steering_pair.on_for_degrees(0,10,20)
    sleep(0.01)

def acompanhar_com_dir(cor_parada):
    while cor('dir')!=cor_parada:
        while cor('dir')=='azul' or cor('dir')=='amarelo' or cor('dir')=='vermelho':
            steering_pair.on(-20,15)
        else:
            steering_pair.off()
        while cor('dir') == 'preto':
            steering_pair.on(5,15)
        else:
            steering_pair.off()
        while cor('dir') == 'branco' or cor('dir')=='semcor':
            steering_pair.on(20,15)
        else:
            steering_pair.off()