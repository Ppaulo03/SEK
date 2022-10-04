vermelho = 1; branco = 2; amarelo = 3; verde = 4; azul = 5; preto = 6; vazio = 0

def OnColor(robot, timestep, sensores_cor, rodas, desire_cor):
    rodas.ForwardForDistance(0.1, 0); rodas.Stop()
    while robot.step(timestep) != -1:

        color = sensores_cor.IdentifyColor()
        if color[0] == vazio or color[1] == vazio:
            sensores_cor.Alinhar(rodas,cor=vazio) 
            break

        elif color[1] == branco: rodas.Turn(-1)
 
        elif color[1] != preto and color[1] != 10: rodas.Turn(1) 

        elif color[0] != desire_cor and color[0] != 10: break

        else: rodas.Forward();

    rodas.Stop()
    rodas.BackwardForDistance(0.05)
    rodas.Turn(-90)
    rodas.BackwardForDistance(0.05)
    sensores_cor.Alinhar(rodas)
    rodas.ForwardForDistance(0.05)
    rodas.Turn(-90)
    
def NotColor(robot, timestep, sensores_cor, rodas, desire_cor, side):
    while robot.step(timestep) != -1:
        color = sensores_cor.IdentifyColor()
        
        if color[side] == desire_cor:  break

        elif color[not side] == 10: rodas.Forward()

        elif color[not side] == branco: rodas.Turn(1*(-1+2*side));

        elif color[not side] != preto and color[1] != 10: rodas.Turn(1*(1-2*side));

        else: rodas.Forward();
       
    rodas.ForwardForDistance(0.05)
    rodas.Stop()
        
def AcharCor(robot, timestep, sensores_cor, rodas, tamanho, ordem):

    if tamanho == 0.1: desire_cor = amarelo;
    elif tamanho == 0.15: desire_cor = vermelho;
    else: desire_cor = azul;
    desire_position = ordem.index(desire_cor)

    while robot.step(timestep) != -1:
        color = sensores_cor.IdentifyColor()
        if color[1] == preto or color[1] == 10: rodas.ForwardForDistance(0.01)
        else: position = ordem.index(color[1]); break

    if desire_position == position:
        rodas.Turn()
        OnColor(robot, timestep, sensores_cor, rodas, desire_cor)

    elif desire_position < position:
        rodas.Turn(-90)
        NotColor(robot, timestep, sensores_cor, rodas, desire_cor, True)
        rodas.Turn(90)
        sensores_cor.Alinhar(rodas)
        rodas.ForwardForDistance(0.05)
        rodas.Turn(-90)
        
    else: 
        rodas.Turn()
        NotColor(robot, timestep, sensores_cor, rodas, desire_cor, False)
        OnColor(robot, timestep, sensores_cor, rodas, desire_cor)