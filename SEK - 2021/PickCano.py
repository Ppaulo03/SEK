import math
vermelho = 1; branco = 2; amarelo = 3; verde = 4; azul = 5; preto = 6; vazio = 0

def AcharCano(robot, timestep, sensor_lateral, rodas, sensores_cor, desire_cor):
    while robot.step(timestep) != -1:
        if sensor_lateral.getValue() < 1:
            rodas.Stop()
            return True
        else:
            color = sensores_cor.IdentifyColor()

            if color[0] == vazio or color[1] == vazio: 
                rodas.BackwardForDistance(0.05)
                return False

            if color[1] == preto: rodas.Turn(1)
            elif color[1] != desire_cor and color[1] != 10: return False
            elif color[0] != branco: rodas.Turn(-1)
            else: rodas.Forward()

def MedirCano(robot,timestep, rodas, sensor_lateral, sensors_cor, size):
    flag = False
    while robot.step(timestep) != -1:
        if sensor_lateral.getValue() < 1: rodas.Stop(); break
        else: rodas.Forward()
    
    while robot.step(timestep) != -1:
        if sensor_lateral.getValue() >= 1: rodas.Stop(); break
        elif rodas.re.getValue() >= 1000: rodas.Stop(); flag = True; break 
        else: rodas.Backward()

    rodas.ForwardForDistance(0.02, speed=1)
    distance = 0; tmpi = 0.64; tmpf = 0.672; di=0; df=0
    beggining = robot.getTime()
    last = sensor_lateral.getValue()

    while robot.step(timestep) != -1:
        
        now = sensor_lateral.getValue()
        color = sensors_cor.IdentifyColor()
        time = round(robot.getTime() - beggining, 3)

        rodas.Stop()
        if time == tmpi: di = sensor_lateral.getValue();
        elif time == tmpf: df = sensor_lateral.getValue();

        if now >= 1 or (now - last > 0.2):
            distance = rodas.GetDistance(time,speed=2.5)
            
            break

        elif (last - now) > 0.2:
            beggining = robot.getTime()
            first = sensor_lateral.getValue()
            distance = 0; di=0; df=0   


        else: rodas.Forward(speed = 2.5);

        last = now

    di = round(di,3);df = round(df,3)
    return [distance,di,df, flag]

def AlinharCano(robot,timestep, rodas, sensor_lateral, sensors_cor, size):
    
    [distance, di, df, flag] = MedirCano(robot,timestep, rodas, sensor_lateral, sensors_cor, size)

    if distance < 0.06:
        rodas.ForwardForDistance(0.05)
        return False, 0

    ang = 0;
    while robot.step(timestep) != -1:
        #if(di > (df - 0.001) and di < (df + 0.001)): break
        if(di == df): break

        elif (di > df):
           
            if not rodas.BackwardForDistance(distance/2 - 0.05, speed = 2):
                rodas.Turn(ang)
                rodas.ForwardForDistance(0.02)
                return False, 0 
            rodas.Turn(-15); ang += 15        
            if not rodas.BackwardForDistance(distance, speed = 2):
                rodas.Turn(ang)
                rodas.ForwardForDistance(0.1)
                return False, 0
            
            [distance, di, df, flag] = MedirCano(robot,timestep, rodas, sensor_lateral, sensors_cor, size)
            if flag:
                rodas.Turn(ang)
                rodas.ForwardForDistance(0.2)
                return False, 0
            
        elif(di < df):
            if not rodas.BackwardForDistance(distance, speed = 2):
                rodas.ForwardForDistance(0.1)
                return False
            rodas.Turn(15); ang += -15
    
            [distance, di, df, flag] = MedirCano(robot,timestep, rodas, sensor_lateral, sensors_cor, size)
            if flag:
                rodas.Turn(ang)
                rodas.ForwardForDistance(0.1)
                return False, 0

    rodas.BackwardForDistance(distance/2 + 0.01, speed=2.5)
    rodas.Turn()
    rodas.Stop()
    return True, ang

def AproximarCano(robot, timestep, sensor_frontal, rodas):
    while robot.step(timestep) != -1:
        dist = sensor_frontal.getValue()
        if dist < 0.094: rodas.Backward(speed=1)
        elif dist > 0.095: rodas.Forward(speed=5)
        else:
            rodas.Stop()
            break

def AlinharProGasoduto(robot, timestep, sensores_cor, rodas, garra, ang):
    preto = 6; vazio = 0; direito = False; esquerdo = False;
    rodas.Turn(ang)

    while robot.step(timestep) != -1:
        color = sensores_cor.IdentifyColor()
        if color[0] == preto: direito = True;
        if color[1] == preto: esquerdo = True;
        
        if direito and esquerdo:
            sensores_cor.Alinhar(rodas)
            rodas.BackwardForDistance(0.1)
            rodas.Turn(-90)
            break
        else: rodas.Backward()

    while robot.step(timestep) != -1:
        color = sensores_cor.IdentifyColor()
        if color[0] == vazio or color[1] == vazio:
            rodas.Stop()
            sensores_cor.Alinhar(rodas, cor=vazio)
            rodas.BackwardForDistance(0.15)
            rodas.Turn(-90)
            
            return
        else: rodas.Forward(speed = 15)

def Pegar(garra, rodas):
    
    garra.Tras()
    garra.Abrir()
    garra.Girar(90)
    garra.Descer()
    garra.Fechar()
    garra.Subir()
    garra.Girar(-90)
    garra.Frente()

def PegarCano(robot, timestep, size, sensores_distancia,sensors_cor, rodas, garra):
    
    if size == 0.1: desire_cor = amarelo;
    elif size == 0.15: desire_cor = vermelho;
    else: desire_cor = azul;
    
    while robot.step(timestep) != -1:
        if not AcharCano(robot, timestep, sensores_distancia[2],rodas, sensors_cor, desire_cor):
            rodas.Turn(90)
            return False
        [achou, ang] = AlinharCano(robot,timestep, rodas, sensores_distancia[2], sensors_cor, size)
        if achou: break

    AproximarCano(robot, timestep, sensores_distancia[0], rodas)
    Pegar(garra, rodas)
    rodas.ForwardForDistance(0.4, speed=0) # Sleep
    AlinharProGasoduto(robot, timestep,sensors_cor, rodas, garra, ang)
    return True