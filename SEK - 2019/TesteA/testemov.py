#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MediumMotor, MoveSteering, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor , UltrasonicSensor
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from time import sleep
import math
import os.path

#   DEFINIÇÕES

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

#   FUNÇÕES

def distancia(sensor):
    a1 = sensor.distance_centimeters
    sleep(0.1)
    a2 = sensor.distance_centimeters
    sleep(0.1)
    a3 = sensor.distance_centimeters
    sleep(0.1)
    distancia = max(a1,a2,a3)
    return distancia

def colocar_cano():
    garra_m.on_for_degrees(60, -200)
    garra_m.stop_action = 'hold'
    garra_g.on_for_degrees(40, -820)  # negativo sobe
    garra_g.stop_action = 'hold'

    # #chega pra frente
    steering_pair.on_for_degrees(0,15, 100)

    #gira p direita
    steering_pair.on_for_degrees(50, 15, 2.43*75)

    sleep(3)

    #ré na diagonal
    steering_pair.on_for_degrees(0, -15, 13*32)
 
    sleep(3)
 
    # gira dnvo o contrario do 1 giro 
    steering_pair.on_for_degrees(100, 15, 2.43*-65/2)
 
    sleep(3)
 
    #chega um pouco pra frente(conserta)
    steering_pair.on_for_degrees(-15, 15, 2.43*30)
    sleep(3)

    #elevador desce um pouco
    garra_g.on_for_degrees(40, 180)  # pos desce
    sleep(3)

    #abre garra
    garra_m.on_for_degrees(10, 300)
    sleep(1)

    # gira pra frente
    steering_pair.on_for_degrees(100, 15, 2.43*65/2)
    sleep(1)

    #re invertida (vai pra frentne)
    steering_pair.on_for_degrees(0, -15, 13*-32)
    sleep(1)

    #gira pra esquerda
    steering_pair.on_for_degrees(50, 15, 2.43*-75)
    sleep(1)

#reconhecimento de cor

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

def cor(sensor):        #atualizada 22/out
    s_max_branco = 0.05000
    v_min_branco = 0.70000
    v_max_preto = 0.3000
    v_min_preto = 0.11000
    v_max_vazio = 0.03
    vermelho = (5,0.8612,0.8196)    #rve: componente (H)ue da referencia do (V)ermelho do sensor (E)squerdo
    azul = (210.0,70.0,50.0)
    amarelo = (40.0,0.8588,0.998)
    verde = (120.0,0.8909,0.4314)
    if sensor=='esq':       #definir as referências
        snr = cor_esq
        rgb_max = rgbmax_e  #chamar definir_rgbmax(snr) antes
    if sensor=='dir':
        snr = cor_dir
        rgb_max = rgbmax_d
    rgb_cru = [snr.red,snr.green,snr.blue] #colocar na lista as componentes
    rgb = escalarRGB(rgb_cru,rgb_max)               #escalo pra 255
    hsv = RGBtoHSV(rgb)
    media = (rgb[0]+rgb[2])/2                             #converte pra hsv
    if hsv[2] > v_min_branco and hsv[1] < s_max_branco:
        return 'branco'
    elif hsv[2] < v_max_preto and hsv[2] > v_min_preto:
        return 'preto'
    elif hsv[2] < v_max_vazio:                #se o v está muito baixo, estamos no vazio
        return 'vazio'
    elif (hsv[0] > (verde[0]-25)) and (hsv[0] < (verde[0]+25)):
        return 'verde'
    elif (rgb[1]/(media+1))>2 and 100<hsv[0]<170:
        return 'verde'
    elif (hsv[0] > (azul[0]-15)) and (hsv[0] < (azul[0]+15)):  
        return 'azul'
    elif (hsv[0] < (vermelho[0]+15)) or (hsv[0] > (vermelho[0]+345)):
        return 'vermelho'
    elif (hsv[0] > (amarelo[0]-15)) and (hsv[0] < (amarelo[0]+15)):
        return 'amarelo'
    else:
        return 'semcor'

def autocompletar(cor1, cor2):
    A = {cor1, cor2}
    B = {'azul','vermelho','amarelo'}
    for item in (B-A):
        cor = item
    return cor

#movimentação

def alinhamento(): #alinhamento 2.0 13/set
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
        steering_pair.on_for_degrees(0,10,40)
    sleep(0.01)
    return

def girar_pro_lado(lado,angulo):
    if lado == 'esq':
        steering_pair.on_for_degrees(-60,10,angulo*3.9)
    elif lado == 'dir':
        steering_pair.on_for_degrees(60,10,angulo*3.9)

def acompanhar_gasoduto(passos):
    d_meta = 10
    fator = 3
    for i in range(passos):
        da = usl.distance_centimeters
        steering_pair.on_for_degrees(0,15,64) #anda 2cm
        db = usl.distance_centimeters
        aux_1 = min(0.99, max(-0.99,(abs(da-db)/2)))
        theta = math.asin(aux_1)
        d_real = db*math.cos(theta)
        aux = min(0.99, max(-0.99,(abs(d_meta-d_real)/2)))
        theta_r = math.acos(aux)
        theta_g = math.radians(90) + abs(theta) - abs(theta_r)
        if db > da and d_real > d_meta: #afastando e acima da meta
            steering_pair.on_for_degrees(-100,20,fator*theta_g)
        elif db > da and d_real < d_meta:
            steering_pair.on_for_degrees(100,20,fator*abs(theta-theta_r))
        elif db < da and d_real < d_meta: #aproximando e abaixo da meta
            steering_pair.on_for_degrees(100,20,fator*theta_g)
        elif db < da and d_real > d_meta:
            steering_pair.on_for_degrees(-100,20,fator*abs(theta-theta_r))
        elif db == da and d_real > d_meta:
            steering_pair.on_for_degrees(-100,20,fator*theta)
        elif db == da and d_real < d_meta:
            steering_pair.on_for_degrees(100,20,fator*theta)
        if usl.distance_centimeters > 15 or usf.distance_centimeters < 10:
            break

def ver_tamanho_espaco():
    acompanhar_gasoduto(5)
    sleep(0.5)
    garra_g.on_for_degrees(20,-1150)
    sleep(0.5)
    global cano_10
    cano_10 = (usl.distance_centimeters < 30)
    garra_g.on_for_degrees(20,1150)
    sleep(0.5)
    if not(cano_10):
        acompanhar_gasoduto(3)
        garra_g.on_for_degrees(20,-1150)
        global cano_15
        global cano_20
        cano_15 = (usl.distance_centimeters < 30)
        cano_20 = not(cano_15)
        garra_g.on_for_degrees(20,1150)

def cor_tamanho_cano():
    if cor_esq or cor_dir == 'azul':
        tam_cano = 5
    elif cor_esq or cor_dir == 'vermelho':
        tam_cano = 2.5
    elif cor_esq or cor_dir == 'amarelo':
        tam_cano = 1
    
    return tam_cano

def distancia_min(sensor):
    a1 = sensor.distance_centimeters
    sleep(0.1)

    a2 = sensor.distance_centimeters
    sleep(0.1)

    a3 = sensor.distance_centimeters
    sleep(0.1)

    distancia = min(a1, a2, a3)

    return distancia


def pegar_cano():   
    garra_g.on_for_degrees(40, -360)  # sobe negativo

    sleep(3)

    while (distancia_min(usl) > 50): # robo sai procurando por canos.
        steering_pair.on(0, 10)

    else:
        steering_pair.off() #para pq acho o cano

    steering_pair.on_for_degrees(0, 10, 32*(15)) #anda a quantidade que o robo tem q voltar pra pegar o cano - variavel
    sleep(3)
    steering_pair.on_for_degrees(100, 20, 2.43*-85) # gira 90 graus p esq em direcao do cano p fica de frente

    #func alinhar com a linha

    while(distancia_min(usf) > 10): #sensor lateral tem que estar 6cm em relacao do chao e 6 cm em relacao ao cano
        steering_pair.on(0, 30)
    else:
        steering_pair.off() #para pq acho o cano

    steering_pair.on_for_degrees(100, 20, 2.43*85) #corrige o giro 90 de graus p fica de lado dnvo. gira p direita
    sleep(3)

    x = usl.distance_centimeters
    y = 12*32*x/10

    #chega pra frente
    steering_pair.on_for_degrees(0,15, 100)

    #gira p direita
    steering_pair.on_for_degrees(50, 15, 2.43*75)
    sleep(3)

    #ré na diagonal
    steering_pair.on_for_degrees(0, -15, y)
    sleep(3)
 
    # gira dnvo o contrario do 1 giro 
    steering_pair.on_for_degrees(100, 15, 2.43*-65/2)
    sleep(5)

    while(distancia_min(usl) < 10):
        steering_pair.on(0, 15)
    else:
        steering_pair.off()
        if cor('esq')!='vazio' or cor('dir')!='vazio':

            steering_pair.on_for_degrees(0, -15, 32*5) # volta
            # steering_pair.on_for_degrees(0, -15, 150) # volta
            sleep(2)
            
            garra_g.on_for_degrees(20, 370)  # desce positivo
            sleep(2)
            
            garra_m.on_for_degrees(30, -400) # fechar garra
            sleep(2)
            
            garra_g.on_for_degrees(40, -1200 )  # sobe negativo
        else:
            pass
            #volta
            #vira direita


def pegar_um_cano():   
    garra_g.on_for_degrees(40, -360)  # sobe negativo

    sleep(3)

    while (distancia_min(usl) > 50): # robo sai procurando por canos.
        steering_pair.on(0, 10)

    else:
        steering_pair.off() #para pq acho o cano

    steering_pair.on_for_degrees(0, 10, 32*(15)) #anda a quantidade que o robo tem q voltar pra pegar o cano - variavel
    sleep(3)
    steering_pair.on_for_degrees(100, 20, 2.43*-85) # gira 90 graus p esq em direcao do cano p fica de frente

    #func alinhar com a linha

    while(distancia_min(usf) > 10): #sensor lateral tem que estar 6cm em relacao do chao e 6 cm em relacao ao cano
        steering_pair.on(0, 30)
    else:
        steering_pair.off() #para pq acho o cano

    steering_pair.on_for_degrees(100, 20, 2.43*85) #corrige o giro 90 de graus p fica de lado dnvo. gira p direita
    sleep(3)

    x = usl.distance_centimeters
    y = 12*32*x/10

    #chega pra frente
    steering_pair.on_for_degrees(0,15, 100)

    #gira p direita
    steering_pair.on_for_degrees(50, 15, 2.43*75)
    sleep(3)

    #ré na diagonal
    steering_pair.on_for_degrees(0, -15, y)
    sleep(3)
 
    # gira dnvo o contrario do 1 giro 
    steering_pair.on_for_degrees(100, 15, 2.43*-65/2)
    sleep(5)

    while(distancia_min(usl) < 10):
        steering_pair.on(0, 15)
    else:
        steering_pair.off()
        if cor('esq')!='vazio' or cor('dir')!='vazio':

            steering_pair.on_for_degrees(0, -15, 32*5) # volta
            # steering_pair.on_for_degrees(0, -15, 150) # volta
            sleep(2)
            
            garra_g.on_for_degrees(20, 370)  # desce positivo
            sleep(2)
            
            garra_m.on_for_degrees(30, -400) # fechar garra
            sleep(2)
            
            garra_g.on_for_degrees(40, -1200 )  # sobe negativo
        else:
            pass
            #volta
            #vira direita

def alinhar_ate_achar(cor):
    k = (cor('dir') != cor)
    l = (cor('esq') != cor)
    while k and l:
        alinhamento()                       
        sleep(0.1)
        k = (cor('dir') != cor)
        l = (cor('esq') != cor)

waiting = True

cano_carregado = 15
item_lista = 0
tamanhos = ['azul','vermelho','vermelho','amarelo','amarelo','amarelo','vermelho']
meeting_area = False
no_preto = False
antes_preto = False
no_vazio = False

aprender_cores = False

pegar_cano = False

ir_pro_gasoduto = False

no_gasoduto = False
gasoduto_com_cano = False

buscar_novo_cano = False

while waiting:
    if btn.any():    # Checks if any button is pressed.
        sound.beep()  # Wait for the beep to finish.
        global waiting
        waiting = False
    else:
        sleep(0.01)  # Wait 0.01 second

rgbmax_e = definir_rgbmax('esq')
rgbmax_d = definir_rgbmax('dir')
sound.speak('ok')

def mov_cores():    #começa com ele na cor, vindo perpendicular à linha preta
                    #termina com ele paralelo à linha preta, usl pros canos, pronto pra pegar_um_cano()
    cor_quer = tamanhos[item_lista]
    quer = mapadecores.index(cor_quer)
    cor_esta = cor('esq')
    esta = mapadecores.index(cor_esta)
    
    girar_pro_lado('esq',90)
    if cor('esq') != cor_esta:
        #fazer manobra pra corrigir
        pass
    if quer == esta:
        if esta == 2:
            manobra_antivazio()
        else:
            manobra_normal()
    elif quer > esta:
        if quer == 2:
            alinhar_ate_achar(cor_quer)
            manobra_antivazio()
        else:
            alinhar_ate_achar(cor_quer)
            normal()
    elif quer < esta:
        girar_pro_lado('dir',180)
        alinhar_ate_achar(cor_quer)