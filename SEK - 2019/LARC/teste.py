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
    v_min_preto = 0.09000
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
    rgb_cru1 = [snr.red,snr.green,snr.blue] #colocar na lista as componentes
    sleep(0.05)
    rgb_cru2 = [snr.red,snr.green,snr.blue]
    sleep(0.05)
    rgb_cru3 = [snr.red,snr.green,snr.blue]
    rgb_cru = [0,0,0]
    for i in range(3):
        rgb_cru[i]=(rgb_cru1[i]+rgb_cru2[i]+rgb_cru3[i])/3
    rgb = escalarRGB(rgb_cru,rgb_max)               #escalo pra 255
    hsv = RGBtoHSV(rgb)                             #converte pra hsv
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

dist = []

def distancia_do_corre(sensor):
    a = [0,0,0,0,0,0,0,0,0,0]
    cont = 0
    for i in range(10):
        a[i]=sensor.distance_centimeters
        sleep(0.01)
        cont = cont + a[i]
    media = cont/10
    var = 0
    for i in range(10):
        x = (a[i]-media)**2
        var = var + x
    stdev = (var/10)**0.5
    mr = 0
    c = 0
    for i in range(10):
        if (media-1.5*stdev) < a[i] < (media + 1.5*stdev):
            mr = mr + a[i]
            c = c+1
    if mr == 0:
        resultado = media
    else:
        resultado = mr/c
    return resultado


while waiting:
    if btn.any():    # Checks if any button is pressed.
        sound.beep()  # Wait for the beep to finish.
        global waiting
        waiting = False
    else:
        sleep(0.01)  # Wait 0.01 second

def checar_fim():
    a1 = distancia_do_corre(usl)
    steering_pair.on_for_degrees(0,15,30)
    a2 = distancia_do_corre(usl)
    steering_pair.on_for_degrees(0,-15,60)
    a3 = distancia_do_corre(usl)
    if a2-1>a1 or a3<a1+1:
        return True
    elif a2-1 <= a1:
        steering_pair.on_for_degrees(0,15,30)
        return False
    elif a3 >= a1+1:
        steering_pair.on_for_degrees(0,-15,30)
        return False

def achar_cano(): #começa paralelo ao cano, termina no fim do cano
    achou_fim_cano = False
    achou_cano = False
    while distancia_do_corre(usl)>45:
        steering_pair.on(0,20)
    else:
        steering_pair.off()
        sound.beep()
        steering_pair.off()
        while not(achou_fim_cano):
            sleep(0.02)
            steering_pair.on_for_degrees(0,10,10)
            sleep(0.02)
            d = distancia_do_corre(usl)
            dist.append(d)
            if len(dist)>11: #ter certeza que já tem 10
                a = 0
                for i in range(1,11): #pega os 10 últimos e faz a média
                    aaa = dist[-i]
                    a = a + aaa
                media_dos_7 = a/10
                b = 0
                for i in range(1,11):
                    if abs(dist[-i]-media_dos_7)>5: #marcar quantos resultados tão instáveis
                        b += 1
                if b<3 and not(achou_cano):
                    sleep(1)
                    sound.beep()
                    achou_cano = True
                if b>2 and achou_cano:
                    if checar_fim():
                        achou_fim_cano = True
def manobra_cano(cor_do_cano):    
    if cor_do_cano == 'azul': c = 20
    if cor_do_cano == 'amarelo': c = 10
    if cor_do_cano == 'vermelho': c = 15 
    q = 13.5 - (c/2)
    steering_pair.on_for_degrees(0,10,30*q)
    lm = LargeMotor(ent_motor_esq)
    lm.on_for_degrees(10,-10*90/2.3)
    if distancia_do_corre(usf)>45:
        lm.on_for_degrees(10,10*90/2.3)
        achar_cano()
        q = 13.5 - (c/2)
        steering_pair.on_for_degrees(0,10,30*q)
        lm.on_for_degrees(10,-10*90/2.3)
    while (distancia_do_corre(usf)>7):
        steering_pair.on(0,15)
    else:
        steering_pair.off()
        steering_pair.on_for_seconds(0,15,1)

def pegar_o_cano():
    
    while(distancia_do_corre(usf) < 10):
        steering_pair.on(0, -15) #da re
        sleep(0.3)
    else:
        steering_pair.off()
        #corrige primeiro giro
        steering_pair.on_for_degrees(100, 20, 2.2*(90)) # gira para direita (lateral de frente p cano

    while(distancia_do_corre(usl) > 30):
        steering_pair.on_for_degrees(0, -15, 32*(2)) # da re ate ver o cano
    else :
        steering_pair.on_for_degrees(0, -15, 32*(4))
        x = distancia_do_corre(usl) #x é da distancia do sensor ao cano antes da baliza
        y = 10*32*x/10 #angulo da baliza
    steering_pair.on_for_degrees(0,-15,90)
    achar_cano()
    
    #baliza
    #chega pra frente
    steering_pair.on_for_degrees(0,15,100)

    #gira p direita
    steering_pair.on_for_degrees(50, 15, 2.43*75)
    sleep(0.5)

    #ré na diagonal
    steering_pair.on_for_degrees(0, -15, y)
    sleep(0.5)
    
    # gira dnvo o contrario do 1 giro 
    steering_pair.on_for_degrees(50, 15, 2.43*-75)

    sleep(0.5)

    steering_pair.on_for_degrees(0, 10, 32*(9)) #anda a quantidade que o robo tem q voltar pra pegar o cano - variavel
    sleep(0.5)
            
    garra_g.on_for_seconds(100, 2)  # desce positivo
    sleep(0.5)
            
    garra_m.on_for_degrees(60, -400) # fechar garra
    sleep(0.5)
            
    garra_g.on_for_degrees(40, -1150 )  # sobe negativo


achar_cano()
manobra_cano('vermelho')
pegar_o_cano()