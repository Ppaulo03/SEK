import math

def AcharGasoduto(robot, timestep, sensor_frontal, rodas, sensores_cor):
    speed = 10
    while robot.step(timestep) != -1:
        if sensor_frontal.getValue() < 0.1:  
            rodas.Stop()
            rodas.Turn(-90)
            break
        else: rodas.Forward(speed = speed)
    rodas.ForwardForDistance(0.05)

def GetAngulo(x,y):
    distSensores = math.radians(20)
    d = math.sqrt(math.pow(x,2) + math.pow(y,2) - 2*x*y*math.cos(distSensores))
    sinB = y*math.sin(distSensores)/d
    sigma = -80 + math.degrees(math.asin(sinB))
    return sigma

def Alinhar(robot, timestep, sensor_alinhar, rodas):
    rodas.Stop()
    while robot.step(timestep) != -1:
        sensor1 = sensor_alinhar[0].getValue(); sensor2 = sensor_alinhar[1].getValue();

        if sensor1 > 0.2 or sensor2 > 0.2: return
        else:
            sig = GetAngulo(sensor1, sensor2)
            if abs(sig) > 0.1: rodas.Turn(sig, speed=0.1, alinhando=True)     
            else: return

def Move(robot, timestep, sensor_lateral_baixo, sensor_frontal, sensor_alinhar, sensores_cor, garra, rodas, turns):
    reading = sensor_lateral_baixo.getValue()
    turned = True; vazio = False; vazio = 0;
    color = sensores_cor.IdentifyColor()
    if color[0] == vazio or color[1] == vazio: 
        rodas.Stop()
        vazio = True
    
    elif reading > 0.25:
        rodas.Stop()
       
        rodas.ForwardForDistance(0.14)
        
        garra.Tras(0.04)
        garra.Girar(-90)
        garra.Frente()
        
        rodas.Turn()
        
        while robot.step(timestep) != -1:
            reading = sensor_lateral_baixo.getValue()
            if reading > 0.25: rodas.Forward(speed=5)
            else: break
        
        turns += 1
    
    elif sensor_frontal.getValue() < 0.05:
        rodas.BackwardForDistance(0.04)
        rodas.Stop()
        cont = 0

        garra.Tras(0.04)
        while robot.step(timestep) != -1:
            garra.Girar(10)
            rodas.Turn(-10)
            cont+=1
            if cont == 9: break
        turns -= 1
        garra.Frente()

    else:
        turned = False
        Alinhar(robot, timestep, sensor_alinhar, rodas)
        rodas.Forward()
        
    return [turns, turned, vazio]

def ProcurarVazio(robot, timestep, sensor_lateral_cima,sensor_lateral_baixo,sensor_frontal,sensor_alinhar, sensores_cor,garra, rodas, size, mapear = False, ):
    espaco_vazio = False; vazio = False
    beggining = robot.getTime();diff = 0; turns = 0; distance = 0
    sequencia = []
    while robot.step(timestep) != -1:

        if sensor_lateral_cima.getValue() > 0.5:
            espaco_vazio = True
        else:
            
            if espaco_vazio:
                time = robot.getTime() - beggining - diff
                distance = rodas.GetDistance(time)
                if distance > 0.20: sequencia.append(0.20)
                elif distance > 0.15: sequencia.append(0.15)
                elif distance > 0.10: sequencia.append(0.10)
                if mapear and len(sequencia)>0: return [turns,True,sequencia]
            beggining = robot.getTime()
            diff = 0
            espaco_vazio = False
        
        time = robot.getTime() - beggining - diff

        distance = rodas.GetDistance(time)
        if distance >= size:
            rodas.Stop()

            garra.Tras(0.095)
            garra.Girar(90*turns)
            garra.Frente()
            
            while robot.step(timestep) != -1:
                cores = sensores_cor.IdentifyColor()
                if cores[0] == 0 or cores[1] == 0: return [turns,True,sequencia]
                elif sensor_lateral_baixo.getValue() > 0.25: return [turns,True,sequencia]
                elif sensor_frontal.getValue() < 0.05: return [turns,True,sequencia]
                elif sensor_lateral_cima.getValue() > 0.5: rodas.Forward()
                else: return [turns, True, sequencia]

        tmp = robot.getTime()
        [turns, turned, vazio] = Move(robot, timestep, sensor_lateral_baixo, sensor_frontal, sensor_alinhar, sensores_cor, garra, rodas, turns)
        tmp = robot.getTime() - tmp
        diff = diff + tmp

        if turned: 
            espaco_vazio = False
            beggining = robot.getTime()
            diff = 0
        if vazio:
            rodas.Stop()
            rodas.BackwardForDistance(0.1)
            turns -= 1
            return [turns, False, sequencia]
        
def AlinharVazio(robot, timestep,sensor_frontal, rodas, size):
    if size == 0.20: correctionBack = 0.036; correctionTurn = 0
    elif size == 0.15: correctionBack = 0.03; correctionTurn = 0
    elif size == 0.10: correctionBack = 0.04; correctionTurn = 0

    beggining = robot.getTime()
    rodas.BackwardForDistance((size/2) + correctionBack,speed=2.5)
    dist = rodas.GetDistance(robot.getTime() - beggining, speed= 2.5)

    rodas.Turn(90 + correctionTurn)
    rodas.Stop()
    while robot.step(timestep) != -1:
        if sensor_frontal.getValue() <= 0.13:
            rodas.Stop()
            return
        else: rodas.Forward()

def ColocarCano(robot, timestep, garra, rodas, sensor_frontal, turns):
    angle = -15
    
    rodas.BackwardForDistance(0.05)

    garra.Tras(0.04)
    garra.Girar(90)
    garra.Frente()

    garra.GirarApoioGarra(angle)
    garra.Tras()
    
    cont = 0
    direcao = 1

    while robot.step(timestep) != -1:
        dist = sensor_frontal.getValue()
        contador = 4
    
        if not rodas.ForwardForDistance(dist - 0.06, speed= 1, pos_sensor= garra.haste_sensor):
            rodas.BackwardForDistance(0.05, speed=2)
            cont += 1
            garra.Girar(-5*direcao)
            garra.GirarApoioGarra(cont*5*direcao)    

            if cont == contador:
                garra.Girar(cont*5*direcao)
                garra.GirarApoioGarra(0)
                direcao *= -1
                cont = 0
        
        else: break

    while robot.step(timestep) != -1:
        dist = sensor_frontal.getValue()
        if dist < 0.07: rodas.Backward(speed=1)
        elif dist > 0.08: rodas.Forward(speed=1)
        else: rodas.Stop; break
    
    rodas.Stop()
    garra.Tras()
    garra.Descer(0.065)
    garra.Abrir()
    rodas.Cano = False

    garra.Subir()
    garra.Frente()

    turning = -90 - 90*turns
    if turning >= 360: turning = turning - 360
    if turning == 270: turning = -90

    garra.Girar(turning)
    garra.GirarApoioGarra(0)
    
    
    rodas.BackwardForDistance(0.12, speed=10)
    garra.Fechar()
    
    
def RetornarMeetingArea(robot, timestep, sensores_cor, rodas, turns, sequencia,sensor_lateral_cima,sensor_lateral_baixo,sensor_frontal,sensor_alinhar,garra):
    preto = 6; vazio = 0; azul = 5; verde = 4
    mais_turns = 0
    if len(sequencia) == 0:
        rodas.ForwardForDistance(0.12)
        rodas.Turn(-90)
        [mais_turns, found, sequencia] = ProcurarVazio(robot, timestep, sensor_lateral_cima,sensor_lateral_baixo,sensor_frontal,sensor_alinhar, sensores_cor,garra, rodas, size=100,mapear = True)
        if found: rodas.Turn(90)

    turning = 180 - 90*turns - 90*mais_turns;
    if turning >= 360: turning = turning - 360
    if turning == 270: turning = -90
    rodas.Turn(turning,speed = 15)

    while robot.step(timestep) != -1:
        color = sensores_cor.IdentifyColor() 
        if color[0] == vazio:
            rodas.BackwardForDistance(0.5)
            rodas.Turn(45)
        elif color[1] == vazio:
            rodas.BackwardForDistance(0.5)
            rodas.Turn(-45)

        if color[0] == verde or color[1] == verde:
            rodas.Stop()
            sensores_cor.Alinhar(rodas,cor = azul)
            rodas.ForwardForDistance(0.5)
            rodas.Forward(speed = 15)
        
        elif color[0] == preto or color[1] == preto:
            rodas.Stop()
            sensores_cor.Alinhar(rodas)
            rodas.ForwardForDistance(0.08)
            rodas.ForwardForDistance(0.2, speed = 0)
            garra.GirarReset()
            return sequencia
        else: rodas.Forward(speed = 15)


def DoGasoduto(robot, timestep, sensores_distancia, rodas, sensores_cor, size, garra, sequencia_base):
    sensor_frontal = sensores_distancia[0]
    sensor_lateral_cima = sensores_distancia[1]
    sensor_lateral_baixo = sensores_distancia[2]
    sensor_alinhar = [sensores_distancia[3], sensores_distancia[4]]
    
    AcharGasoduto(robot, timestep, sensor_frontal, rodas, sensores_cor)
    [turns, found, sequencia] = ProcurarVazio(robot, timestep, sensor_lateral_cima,sensor_lateral_baixo,sensor_frontal,sensor_alinhar, sensores_cor,garra, rodas, size)
    if found:
        AlinharVazio(robot, timestep,sensor_frontal, rodas, size)
        ColocarCano(robot, timestep, garra, rodas, sensor_frontal, turns)
        
    for v in sequencia:
        if v not in sequencia_base: sequencia.remove(v)
    sequencia = RetornarMeetingArea(robot, timestep, sensores_cor, rodas, turns, sequencia, sensor_lateral_cima, sensor_lateral_baixo, sensor_frontal, sensor_alinhar, garra)
    return [found, sequencia]