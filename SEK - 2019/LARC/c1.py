#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MediumMotor, MoveSteering, MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
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
tank = MoveTank(ent_motor_esq,ent_motor_dir)
tank.cs = ColorSensor(ent_sc_esq)
garra_g = LargeMotor(ent_motor_grande)
garra_m = MediumMotor(ent_motor_medio)

cor_esq = ColorSensor(ent_sc_esq)
cor_dir = ColorSensor(ent_sc_dir)
usl = UltrasonicSensor(ent_us_lat)
usf = UltrasonicSensor(ent_us_fr)

sound = Sound()
btn = Button()

#Funções

    #Cor
    #Locomoção

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

    #Locomoção

def alinhamento(): #alinhamento 2.0 13/set
    cor_esq_inicial = cor('esq')
    cor_dir_inicial = cor('dir')
    while cor_dir_inicial==cor('dir') and cor('esq')==cor_esq_inicial:
        steering_pair.on(0,27)
    else:
        steering_pair.off()
        sleep(0.01)
    cor_aux_e = cor('esq')
    cor_aux_d = cor('dir')
    if cor('esq')==cor('dir'):
        steering_pair.off()
    elif cor_dir_inicial!=cor_aux_d:
        while cor('esq')==cor_aux_e:
            steering_pair.on(60,10)
        else:
            steering_pair.off()
        steering_pair.on_for_degrees(0,10,10)
    else:
        while cor('dir')==cor_aux_d:
            steering_pair.on(-60,10)
        else:
            steering_pair.off()
        steering_pair.on_for_degrees(0,10,40)
    sleep(0.01)

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
            LargeMotor(ent_motor_esq).on(-10)
        else:
            LargeMotor(ent_motor_esq).off()
        steering_pair.on_for_degrees(0,10,20)
    else:
        while cor('dir')==cor_aux_d:
            LargeMotor(ent_motor_dir).on(-10)
        else:
            LargeMotor(ent_motor_dir).off()
        steering_pair.on_for_degrees(0,10,20)
    sleep(0.01)


def testar_preto():
    steering_pair.on_for_degrees(0,10,150)
    if (cor('esq')!='azul' and cor('esq')!='vermelho' and cor('esq')!='amarelo'):
        steering_pair.on_for_degrees(0,-10,150)
        return False
    else:
        steering_pair.on_for_degrees(0,-10,150)
        return True

def girar_pro_lado(lado,angulo):
    if lado == 'esq':
        steering_pair.on_for_degrees(-60,10,angulo*3.9)
    elif lado == 'dir':
        steering_pair.on_for_degrees(60,10,angulo*3.9)

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

def acompanhar_gasoduto(passos,d_meta):
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
        if cor('esq')=='vazio' or cor('dir')=='vazio':
            global voltar_com_cano
            global buscar_novo_cano
            global no_gasoduto
            voltar_com_cano = True
            no_gasoduto = False
            buscar_novo_cano = True

def distancia(sensor):
    a1 = sensor.distance_centimeters
    sleep(0.05)
    a2 = sensor.distance_centimeters
    sleep(0.05)
    a3 = sensor.distance_centimeters
    sleep(0.05)
    a4 = sensor.distance_centimeters
    sleep(0.05)
    a5 = sensor.distance_centimeters
    sleep(0.05)
    a6 = sensor.distance_centimeters
    sleep(0.05)
    a7 = sensor.distance_centimeters
    sleep(0.05)
    media = (a1+a2+a3+a4+a5+a6+a7)/7.0
    return media

def distancia_min(sensor):
    a1 = sensor.distance_centimeters
    sleep(0.05)
    a2 = sensor.distance_centimeters
    sleep(0.05)
    a3 = sensor.distance_centimeters
    sleep(0.05)
    a4 = sensor.distance_centimeters
    sleep(0.05)
    a5 = sensor.distance_centimeters
    sleep(0.05)
    return min(a1,a2,a3,a4,a5)

def ver_tamanho_espaco(): #começa e termina com a garra em cima
    cont = 0
    while distancia(usl)>35:
        steering_pair.on_for_degrees(0,10,10)
        cont = cont + 10
    cm = cont/30
    global cano_10
    global cano_15
    global cano_20
    cano_10 = (cm < 15)
    cano_15 = cm > 15 and cm < 20
    cano_20 = cm > 20

def pegar_um_cano():   
    garra_g.on_for_seconds(100, 2)
    sleep(1)

    garra_m.on_for_degrees(60, 200)

    garra_g.on_for_degrees(40, 32*(-10))
    sleep(3)

    while (distancia_min(usl) > 60): 
        steering_pair.on(0, 20) # robo sai procurando por canos.

        #funcao alinha
    else:
        steering_pair.off() # para pq achou o cano
        sleep(1)
        distancia_1 = usl.distance_centimeters
        
        steering_pair.on_for_degrees(100, 20, 2.2*(-90)) # gira para esquerda (frontal de frente p cano)
        sleep(0.5)
        steering_pair.on_for_degrees(0, 15, 32*(distancia_1/2))
        sleep(0.5)
        steering_pair.on_for_degrees(100, 20, 2.2*(90)) # gira de voltA (lateral de frente p cano)

    while (distancia_min(usl) > 60 - distancia_1):
        steering_pair.on(0, 20)
    else:
        steering_pair.off()

    while (distancia_min(usl) < 60 - distancia_1): #andar ate chegar ao final do cano
        steering_pair.on(0, 20)
    else:
        steering_pair.off() 
        steering_pair.on_for_degrees(0, -15, 32*(6)) #da uma re pra concertar o erro

    steering_pair.on_for_degrees(100, 20, 2.2*(-90)) # gira para esquerda (frontal de frente p cano)

    while(usf.distance_centimeters > 7):
        steering_pair.on(0, 15) #empurra o cano
        sleep(0.3)
    else:
        steering_pair.off()
        steering_pair.on_for_seconds(0,20, 1) 
        sleep(0.5)
    
    while(usf.distance_centimeters < 10):
        steering_pair.on(0, -15) #da re
        sleep(0.3)
    else:
        steering_pair.off()
        #corrige primeiro giro
        steering_pair.on_for_degrees(100, 20, 2.2*(90)) # gira para direita (lateral de frente p cano

    while(distancia_min(usl) > 30):
        steering_pair.on_for_degrees(0, -15, 32*(2)) # da re ate ver o cano
    else :
        steering_pair.on_for_degrees(0, -15, 32*(4))
        x = distancia_min(usl) #x é da distancia do sensor ao cano antes da baliza
        y = 10*32*x/10 #angulo da baliza

    while(distancia_min(usl) < 20):
        steering_pair.on(0, 10)
    else:
        steering_pair.off() #para pq n ve mais o cano
    
    while(distancia_min(usl) > 20):
        steering_pair.on(0, -10)
    else :
        steering_pair.off()

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

    steering_pair.on_for_degrees(0, 10, 32*(7)) #anda a quantidade que o robo tem q voltar pra pegar o cano - variavel
    sleep(0.5)
            
    garra_g.on_for_seconds(100, 2)  # desce positivo
    sleep(0.5)
            
    garra_m.on_for_degrees(60, -400) # fechar garra
    sleep(0.5)
            
    garra_g.on_for_degrees(40, -1150 )  # sobe negativo


def colocar_cano():
    # dist sensor -> gasoduto = 10cm
    garra_g.on_for_degrees(40, -820)  # negativo sobe
    garra_g.stop_action = 'hold'

    #chega pra frente
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


# Variáveis

waiting = True
antes_preto = False
no_vazio = False

aprender_cores = False

pegar_cano = False

no_gasoduto = False

voltar_com_cano = False

tamanhos=['vermelho','azul','vermelho']
item_lista = 0
# Começo

while waiting:
    if btn.any():
        sound.beep() 
        global waiting
        global meeting_area
        waiting = False
        meeting_area = True
    else:
        sleep(0.01)  # Wait 0.01 second

rgbmax_e = definir_rgbmax('esq')
rgbmax_d = definir_rgbmax('dir')
garra_g.on_for_seconds(10,1.5)
garra_m.on_for_seconds(10,1)
mapadecores=['vermelho','amarelo','azul']

while True:
    while meeting_area: #começa aleatoriamente na meeting area
                        #termina com os sensores de cor no vazio certo
        sound.beep()
        while cor('esq')=='branco' and cor('dir')=='branco':
            steering_pair.on(0,15)
        else:
            steering_pair.off()
        steering_pair.on_for_degrees(0,-15,70)
        alinhamento()
        steering_pair.on_for_degrees(0,10,70)
        if cor('esq')=='vazio' or cor('dir')=='vazio':
            global no_vazio
            no_vazio = True
            if cor('esq')!=cor('dir'):
                steering_pair.on_for_degrees(0,-15,150)
                alinhamento()
            steering_pair.on_for_degrees(0,-25,350) #volta e vira pra esquera
            girar_pro_lado('esq',90)
            sound.speak('empty')
        elif (cor('esq')!='vazio' and cor('dir')!='vazio'):
            a = testar_preto()
            if a: #está no preto
                steering_pair.on_for_degrees(0,-20,350) #volta e vira pra direita
                girar_pro_lado('dir',90)
                sound.speak('black')
                
                while cor('esq')!='vazio' and cor('dir')!='vazio':
                    while cor('esq')=='branco' and cor('dir')=='branco':
                        steering_pair.on(0,15)
                    else:
                        steering_pair.off()
                    while cor('esq')!='branco':
                        steering_pair.on(20,15)
                    else:
                        steering_pair.off()
                    while cor('dir')!='branco':
                        steering_pair.on(-20,15)
                    else:
                        steering_pair.off()

                steering_pair.on_for_degrees(0,-15,150)
                alinhamento()               
                global meeting_area
                global aprender_cores
                meeting_area = False
                pegar_cano = True        
            else: #está na rampa
                steering_pair.on_for_degrees(0,-20,350) #volta e vira pra esquerda
                sound.speak('green')
                girar_pro_lado('esq',180)



    while aprender_cores:   #começa virado pro vazio certo
                            #termina virado pro vazio certo
        sound.beep()
        sound.beep()
        h = os.path.exists("cores.txt")
        if h:
            global aprender_cores
            global mapadecores
            mapadecores = [line.rstrip('\n') for line in open("cores.txt")] # pra ler o arquivo pra lista de novo
            aprender_cores = False
            pegar_cano = True
        else:                            #verificar se já existe o arquivo, se não existir:
            cores = open("cores.txt", "w+")     #cria o arquivo 
            cores.close()                       #fecha o arquivo
            steering_pair.on_for_degrees(0,-20,350)
            girar_pro_lado('esq',90)            #90 graus pra esquerda
            alinhamento()                       #achou a faixa preta
            steering_pair.on_for_degrees(0,20,200)
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
            while cor('esq')!='branco' or cor('dir')!='branco':
                steering_pair.on(0,-20) #vai pro branco
            else:
                steering_pair.off()
            steering_pair.on_for_degrees(0,-20,100)
            alinhamento()                       #alinhou no preto (ou na cor)
            steering_pair.on_for_degrees(0,-20,450) #voltou
            girar_pro_lado('dir',90)
            sound.beep()
            sound.beep()
    while pegar_cano:
        #começa com os sensores no vazio certo (ou virados pra ele)
        #termina
        steering_pair.on_for_degrees(0,-20,350) #dá ré
        sleep(2)
        girar_pro_lado('esq',180)               #meia volta
        sleep(2)
        cor_desejada = tamanhos[item_lista]
        acompanhar_com_dir(cor_desejada)        #acompanha a faixa preta com o sensor direito até achar a cor desejada
        indice_cor_desejada = mapadecores.index(cor_desejada)
        if indice_cor_desejada == 2:
            acompanhar_com_dir('vazio')
            steering_pair.on_for_degrees(0,-15,250)
        else:
            acompanhar_com_dir(mapadecores[(indice_cor_desejada+1)])
        girar_pro_lado('esq',180)
        pegar_um_cano()
        #forçando, depois colocar dentro da função acima #ou não
        if cor_desejada == 'azul':
            global cano_carregado
            cano_carregado = 20
        elif cor_desejada == 'vermelho':
            global cano_carregado
            cano_carregado = 15
        
        girar_pro_lado('dir',90) #prepara pra sair
        while cor('esq')!='branco' or cor('dir')!='branco': #acha o branco
            steering_pair.on(0,15)
        else:
            steering_pair.off()
        alinhamento_pra_tras()
        steering_pair.on_for_degrees(0,20,450)
        girar_pro_lado('esq',85)
        alinhamento() #chegou no vazio certo

        steering_pair.on_for_degrees(0,-20,350)
        girar_pro_lado('dir',90)
        while cor('dir')!='azul': #desce de frente e sobe de costas
            steering_pair.on(2,40)
        else:
            steering_pair.off()
        steering_pair.on_for_degrees(0,60,250)

        while usf.distance_centimeters > 16:
            steering_pair.on(0,15)
        else:
            steering_pair.off()
        girar_pro_lado('esq',90)
        alinhamento()
        steering_pair.on_for_degrees(0,-20,350)
        girar_pro_lado('esq',180)
        garra_g.on_for_degrees(20,-1080) #subir a garra
        global gasoduto_com_cano
        gasoduto_com_cano = (usl.distance_centimeters<20)
        garra_g.on_for_degrees(20,1080) #desce a garra
        pegar_cano = False
        no_gasoduto = True
    while no_gasoduto:
        while gasoduto_com_cano and distancia(usl) < 15 and distancia(usf) > 12:
            acompanhar_gasoduto(4,10)
            
            if gasoduto_com_cano and distancia(usl) < 15 and distancia(usf) > 12:
                garra_g.on_for_degrees(20,-1080)
                sleep(0.1)
                global gasoduto_com_cano
                gasoduto_com_cano = (distancia_min(usl) < 25)
                if gasoduto_com_cano:
                    sound.speak('ok')
                sleep(0.01)
                garra_g.on_for_degrees(20,1080)
                sleep(0.01)
            
            while gasoduto_com_cano and usf.distance_centimeters < 12:  
                steering_pair.on_for_degrees(0,-10,150)
                girar_pro_lado('dir',90) #ver se ele não para perto demais da nova lateral
                sleep(3)
            
            while gasoduto_com_cano and usl.distance_centimeters > 15 and usf.distance_centimeters > 12:
                steering_pair.on_for_degrees(0,10,100)
                girar_pro_lado('esq',90)
                sleep(3)

            while not(gasoduto_com_cano):
                garra_g.on_for_degrees(20,-1100) #sobe a garra
                while distancia(usl) > 35:
                    steering_pair.on(0,-10)
                else:
                    steering_pair.off()
                    sound.speak('pipe')
                    sleep(0.01)
                while distancia(usl) < 35:
                    steering_pair.on(0,10)
                else:
                    steering_pair.off()
                    sleep(0.01)
                ver_tamanho_espaco()
                if (cano_carregado == 10 and cano_10) or (cano_carregado == 15 and cano_15) or (cano_carregado == 20 and cano_20):
                    colocar_cano()
                    global cano_carregado
                    cano_carregado = 0
                else:
                    garra_g.on_for_degrees(10,1100)
                    acompanhar_gasoduto(9,10)
                global gasoduto_com_cano
                gasoduto_com_cano = not(cano_carregado==0)
                no_gasoduto = gasoduto_com_cano
            no_gasoduto = not(cano_carregado == 0)
            sound.beep()
            sound.beep()
            sound.beep()
        