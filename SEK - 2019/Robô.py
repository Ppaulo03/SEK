#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MediumMotor, MoveSteering, MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor , UltrasonicSensor
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from time import sleep
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('robô.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(message)s'))
logger.addHandler(file_handler)

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

class Robot:

    def __init__ (self):
        self.ent_motor_esq = OUTPUT_C
        self.ent_motor_dir = OUTPUT_D
        self.ent_motor_grande = OUTPUT_B
        self.ent_motor_medio = OUTPUT_A
        self.ent_sc_esq = INPUT_3
        self.ent_sc_dir = INPUT_4
        self.ent_us_lat = INPUT_2
        self.ent_us_fr = INPUT_1
        self.mapadecores=['amarelo','vermelho','azul']
        self.tamanhos=['vermelho','vermelho','amarelo','azul']
        self.item_lista = 0

    def steering_pair(self):
        return MoveSteering(self.ent_motor_esq, self.ent_motor_dir)

    def tank(self):
        return MoveTank(self.ent_motor_esq,self.ent_motor_dir)
    
    def garra_g(self):
        return LargeMotor(self.ent_motor_grande)
   
    def garra_m(self):
        return MediumMotor(self.ent_motor_medio)

    def cor_esq(self):
        return ColorSensor(self.ent_sc_esq)

    def cor_dir(self):
        return ColorSensor(self.ent_sc_dir)

    def usl(self):
        return UltrasonicSensor(self.ent_us_lat)

    def usf(self):
        return UltrasonicSensor(self.ent_us_fr)
    
    def sound(self):
        return Sound()

    def btn(self):
        return Button()

    def girar_pro_lado(self,lado,angulo):
        if lado == 'esq':
            self.steering_pair().on_for_degrees(-60,10,angulo*3.9)
        elif lado == 'dir':
            self.steering_pair().on_for_degrees(60,10,angulo*3.9)
        else:
            print("ERRO")
            
    def definir_rgbmax(self,snr):
        if snr=='esq':
            sensor=self.cor_esq()
        else:
            sensor=self.cor_dir()
        rgbmax = [sensor.red,sensor.green,sensor.blue]
        logger.debug('rgbmax = {}'.format(rgbmax))
        return rgbmax
   
    def set_rgbmax(self):
        self.rgbmax_esq = self.definir_rgbmax('esq')
        self.rgbmax_dir = self.definir_rgbmax('dir')

    def rgbmax_e(self):
        return self.rgbmax_esq

    def rgbmax_d(self):
        return self.rgbmax_dir

    def cor(self,sensor):        
        s_max_branco = 0.05_000
        v_min_branco = 0.70_000
        v_max_preto = 0.3_000
        v_min_preto = 0.09_000
        v_max_vazio = 0.03
        vermelho = (5, 0.8612, 0.8196) 
        azul = (210.0, 70.0, 50.0)
        amarelo = (40.0, 0.8588, 0.998)
        if sensor=='esq':     
            snr = self.cor_esq()
            rgb_max = self.rgbmax_esq
        if sensor=='dir':
            snr = self.cor_dir()
            rgb_max = self.rgbmax_dir
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
        logger.debug('rgbmax_dir = {}\nself.rgbmax_esq = {}'.format(self.rgbmax_dir,self.rgbmax_esq))                      
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

    def testar_preto(self):
        self.steering_pair().on_for_degrees(0,10,150)
        if (self.cor('esq')!='azul' and self.cor('esq')!='vermelho' and self.cor('esq')!='amarelo'):
            self.steering_pair().on_for_degrees(0,-10,150)
            return False
        else:
            self.steering_pair().on_for_degrees(0,-10,150)
            return True

    def alinhamento(self): 
        cor_esq_inicial = self.cor('esq')
        cor_dir_inicial = self.cor('dir')
        while cor_dir_inicial==self.cor('dir') and self.cor('esq')==cor_esq_inicial:
            self.steering_pair().on(0,20)
        else:
            self.steering_pair().off()
            sleep(0.01)
        cor_aux_e = self.cor('esq')
        cor_aux_d = self.cor('dir')
        if self.cor('esq')==self.cor('dir'):
            self.steering_pair().off()
        elif cor_dir_inicial!=cor_aux_d:
            while self.cor('esq')==cor_aux_e:
                LargeMotor(self.ent_motor_esq).on(10)
            else:
                self.steering_pair().off()
            self.steering_pair().on_for_degrees(0,10,10)
        else:
            while self.cor('dir')==cor_aux_d:
                LargeMotor(self.ent_motor_dir).on(10)
            else:
                self.steering_pair().off()
            self.steering_pair().on_for_degrees(0,10,40)
        sleep(0.01)
        logger.debug('cor_dir = {}, cor_esq = {}'.format(self.cor('dir'),self.cor('esq')))

    def alinhamento_pra_tras(self): 
        cor_esq_inicial = self.cor('esq')
        cor_dir_inicial = self.cor('dir')
        while cor_dir_inicial==self.cor('dir') and self.cor('esq')==cor_esq_inicial:
            self.steering_pair().on(0,-15)
        else:
            self.steering_pair().off()
            sleep(0.01)
        cor_aux_e = self.cor('esq')
        cor_aux_d = self.cor('dir')
        if self.cor('esq')==self.cor('dir'):
            self.steering_pair().off()
        elif cor_dir_inicial!=cor_aux_d:
            while self.cor('esq')==cor_aux_e:
                LargeMotor(self.ent_motor_esq).on(-10)
            else:
                LargeMotor(self.ent_motor_esq).off()
            self.steering_pair().on_for_degrees(0,10,20)
        else:
            while self.cor('dir')==cor_aux_d:
                LargeMotor(self.ent_motor_dir).on(-10)
            else:
                LargeMotor(self.ent_motor_dir).off()
            self.steering_pair().on_for_degrees(0,10,20)
        sleep(0.01)

    def acompanhar_com_dir(self,cor_parada):
        while self.cor('dir')!=cor_parada:
            while self.cor('dir')=='azul' or self.cor('dir')=='amarelo' or self.cor('dir')=='vermelho':
                self.steering_pair().on(-20,15)
            else:
                self.steering_pair().off()
            while self.cor('dir') == 'preto':
                self.steering_pair().on(5,15)
            else:
                self.steering_pair().off()
            while self.cor('dir') == 'branco' or self.cor('dir')=='semcor':
                self.steering_pair().on(20,15)
            else:
                self.steering_pair().off()

    def set_mapa_de_cores(self,mapa):
        self.mapadecores = mapa

    def get_mapa_de_cores(self):
        return self.mapadecores

    def get_tamanho(self):
        return self.tamanhos

    def get_index(self):
        return self.item_lista

    def set_index(self):
        self.item_lista +=1