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
    # Reconhecimento de cor
        # RGBtoHSV
        # escalarRGB
        # definir_rgbmax
        # cor
        # autocompletar
    # Movimentação
        #alinhamento
        #girar_pro_lado

# Reconhecimento de cor

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
    rgb_cru = [snr.red,snr.green,snr.blue] #colocar na lista as componentes
    rgb = escalarRGB(rgb_cru,rgb_max)               #escalo pra 255
    hsv = RGBtoHSV(rgb)
    media = (rgb[0]+rgb[2])/2                             #converte pra hsv
    if hsv[2] > v_min_branco and hsv[1] < s_max_branco:
        return 'branco'
    elif (rgb[1]/(media+1))>2 and 100<hsv[0]<170:
        return 'verde'
    elif hsv[2] < v_max_preto and hsv[2] > v_min_preto:
        return 'preto'
    elif hsv[2] < v_max_vazio:                #se o v está muito baixo, estamos no vazio
        return 'vazio'
    elif (hsv[0] > (verde[0]-25)) and (hsv[0] < (verde[0]+25)):
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

# Movimentação

def alinhamento(): #alinhamento 2.0 13/set
    cor_esq_inicial = cor('esq')
    cor_dir_inicial = cor('dir')
    while cor_dir_inicial==cor('dir') and cor('esq')==cor_esq_inicial:
        steering_pair.on(0,25)
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

def pegar_um_cano():   
    garra_g.on_for_seconds(100, 2) #garante o elevador em baixo
    sleep(1)
    garra_m.on_for_degrees(60, 200) #abre a garra
    garra_g.on_for_degrees(40, 32*(-10))  # sobe negativo
    sleep(3)
    while (usl.distance_centimeters>60):
        steering_pair.on(0,30)
    else:
        steering_pair.off() 
    sleep(0.5)
    steering_pair.on_for_degrees(0,20,32)
    x1 = usl.distance_centimeters
    steering_pair.on_for_degrees(0, 15, 32*(8))
    sleep(1)
    x2 = usl.distance_centimeters
    ang_cano = math.atan(abs(x1 - x2)/8)
    ang = abs(math.degrees(ang_cano))
    sound.beep()
    if(x1 > x2):
        steering_pair.on_for_degrees(50, 30, 2.428*ang)
    else:
        steering_pair.on_for_degrees(50, 30, 2.428*-ang) 
    
    #se giro em torno do meio do robo *2.428
    #se giro for em cima de 1 roda *2
    steering_pair.on_for_degrees(0, 15, 32*(15)) #anda 15 cm pra frente
    steering_pair.on_for_degrees(100, 20, 2.2*(-90)) # gira 90 graus p esq em direcao do cano p fica de frente

    while(distancia_media(usf) > 15):
        steering_pair.on(0, 20)
    else:
        steering_pair.off() #para pq achou o cano

    steering_pair.on_for_degrees(100, 20, 2.2*90) #corrige o giro 90 de graus p fica de lado dnvo. gira p direita
    sleep(3)

    while(usl.distance_centimeters > 20):
        steering_pair.on_for_degrees(0, -15, 32*(2)) # sensor n ve o cano, entao da re
    else :
        x3 = usl.distance_centimeters #x3 é da distancia do sensor ao cano antes da baliza
        y = 10*32*x3/10 #angulo da baliza

    # while(us_lat.distance_centimeters < 20):
    #     steering_pair.on_for_degrees(0, 15, 32*(2))
    # else:
    #     steering_pair.off() #para pq n ve mais o cano
    
    while(usl.distance_centimeters > 20):
        steering_pair.on_for_degrees(0, -15, 32)
    else :
        steering_pair.off()

    #inicio baliza

    #chega pra frente
    steering_pair.on_for_degrees(0,15,190)

    #gira p direita
    steering_pair.on_for_degrees(50, 15, 2.43*75)
    sleep(3)

    #ré na diagonal
    steering_pair.on_for_degrees(0, -15, y)
    sleep(3)
    
    # gira dnvo o contrario do 1 giro 
    steering_pair.on_for_degrees(50, 15, 2.43*-75)

    sleep(5)

    # steering_pair.on_for_degrees(0, -15, 32*(2))

    steering_pair.on_for_degrees(0, 10, 32*(3)) #anda a quantidade que o robo tem q voltar pra pegar o cano - variavel
    sleep(3)
            
    garra_g.on_for_seconds(100, 2)  # desce positivo
    sleep(2)
            
    garra_m.on_for_degrees(60, -400) # fechar garra
    sleep(2)
            
    garra_g.on_for_degrees(40, -1150 )  # sobe negativo

def mov_cores():    #começa com ele na cor, vindo perpendicular à linha preta
                    #termina com ele paralelo à linha preta, usl pros canos, pronto pra pegar_um_cano()
    cor_quer = tamanhos[item_lista]
    quer = mapadecores.index(cor_quer)
    cor_esta = cor('esq')
    esta = mapadecores.index(cor_esta)
    steering_pair.on_for_degrees(0,-20,200) #ré
    alinhamento()
    girar_pro_lado('esq',90) #vira pra esquerda
    if quer == esta:
        if esta == 2:
            while cor('dir')!='vazio' and cor('esq')!='vazio': #vai até achar o vazio
                steering_pair.on(0,20)
            else:
                steering_pair.off()
                steering_pair.on_for_degrees(0,-10,100)
                alinhamento()
                steering_pair.on_for_degrees(0,-20,350)
                girar_pro_lado('dir',180)
        else:
            while cor('dir')!= mapadecores[quer+1]:#vai até achar cor + 1
                steering_pair.on(0,30)
            else:
                steering_pair.off()
                steering_pair.on_for_degrees(0,20,100)
                girar_pro_lado('dir',180)
    elif quer > esta:
        if quer == 2:
            while cor('dir')!='vazio' and cor('esq')!='vazio':
                steering_pair.on(0,20)
            else:
                steering_pair.off()
                steering_pair.on_for_degrees(0,-10,100)
                alinhamento()
                steering_pair.on_for_degrees(0,-20,350)
                girar_pro_lado('dir',180)
                sound.beep()
        else:
            while cor('dir')!=mapadecores[1] and cor('esq')!=mapadecores[1]:
                steering_pair.on(0,20)
            else:
                steering_pair.off()
                steering_pair.on_for_degrees(0,10,100)
                girar_pro_lado('dir',180)
                sound.beep()
    elif quer < esta:
        girar_pro_lado('dir',180)
        while cor('dir')!=mapadecores[quer] and cor('esq')!=mapadecores[quer]:
            steering_pair.on(0,20)
        else:
            steering_pair.off()
            sound.beep()

# HERE COMES THE CLEITON, TCHURURURU

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

buscar_novo_cano = False

while waiting:
    if btn.any():    # Verifica se algum botão foi pressionado
        sound.beep()
        global waiting
        global meeting_area
        waiting = False
        meeting_area = True
    else:
        sleep(0.01)

rgbmax_e = definir_rgbmax('esq')
rgbmax_d = definir_rgbmax('dir')

while True:
    while meeting_area: #começa aleatoriamente na meeting area
                        #termina com os sensores de cor no vazio certo
        sound.beep()
        alinhamento()
        #steering_pair.on_for_degrees(0,10,30)
        no_vazio = (cor('esq')=='vazio' or cor('esq')=='semcor') and (cor('dir')=='vazio' or cor('dir')=='semcor')
        no_preto = (cor('esq')=='preto' or cor('dir')=='preto')
        if no_preto:
            #sound.beep()
            #sound.speak('black')
            steering_pair.on_for_degrees(0,-20,300)
            girar_pro_lado('dir',90)
            global antes_preto
            antes_preto = True
        else:
            if (cor('esq')=='verde' or cor('dir')=='verde'):
                #sound.beep()
                #sound.speak('green')
                steering_pair.on_for_degrees(0,-20,300)
                girar_pro_lado('dir',180)
            elif (no_vazio and not(antes_preto)):
                #sound.beep()
                #sound.speak('not ok')
                steering_pair.on_for_degrees(0,-20,300)
                girar_pro_lado('dir',90)    
        meeting_area = not(no_vazio and antes_preto)

    while aprender_cores:   #começa com os sensores de cor no vazio certo
                            #termina virado pro vazio certo
        h = os.path.exists("cores.txt")
        if h:
            global aprender_cores
            global mapadecores
            mapadecores = [line.rstrip('\n') for line in open("cores.txt")] # pra ler o arquivo pra lista de novo
            aprender_cores = False
        else:                            #verificar se já existe o arquivo, se não existir:
            cores = open("cores.txt", "w+")     #cria o arquivo 
            cores.close()                       #fecha o arquivo
            steering_pair.on_for_degrees(0,-20,350)
            girar_pro_lado('esq',90)            #90 graus pra esquerda
            alinhamento()                       #achou a faixa preta
            steering_pair.on_for_degrees(0,20,100)
            girar_pro_lado('esq',90)
            cor1 = cor('dir')                #salvar primeira cor
            while cor('dir')==cor1 or cor('dir')=='preto':
                while cor('dir')!='preto':
                    steering_pair.on(-10,15)
                else:
                    steering_pair.off()
                    steering_pair.on_for_degrees(50,15,100)
            cor2 = cor('dir')                #salvar segunda cor
            cor3 = autocompletar(cor1, cor2)    #autocompletar 3a cor
            cores = open("cores.txt","a")
            escrever = [cor1,'\n',cor2,'\n',cor3]
            cores.writelines(escrever)
            cores.close()
            sound.beep()
            girar_pro_lado('dir',80) #ficou na cor
            steering_pair.on_for_degrees(0,-20,200) #voltou
            alinhamento()                       #alinhou no preto (ou na cor)
            steering_pair.on_for_degrees(0,-20,350) #voltou
            girar_pro_lado('dir',90)
            sound.beep()
            sound.beep()
while pegar_cano:   #começa virado pro vazio certo
                    #terminar com os sensores no vazio certo
    sound.speak('pipe')
    girar_pro_lado('esq',90) 
    if cor('esq')=='branco' or cor('dir')=='branco':
        alinhamento()
    steering_pair.on_for_degrees(0,20,120)
    mov_cores()
    pegar_um_cano() #dentro dessa função tem que ter a mudança de pegar_cano (e a rotina pra caso ele não consiga pegar o cano)
    cor_atual = cor('esq')
    girar_pro_lado('dir',90)
    alinhamento()
    m = cor('esq') != 'preto'
    n = cor('dir') != 'preto'
    while m or n:
        girar_pro_lado('dir',90)
        alinhamento()
        m = cor('esq') != 'preto'
        n = cor('dir') != 'preto'
    steering_pair.on_for_degrees(0,25,450)
    girar_pro_lado('esq',90)
    alinhar_ate_achar('vazio')
    pegar_cano = False
    ir_pro_gasoduto = True

