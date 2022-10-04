vermelho = 1; branco = 2; amarelo = 3; verde = 4; azul = 5; preto = 6; vazio = 0

Ordem = []

def EncontrarPreto(robot, timestep, sensores_cor, rodas):
    while robot.step(timestep) != -1:
        
        color = sensores_cor.IdentifyColor()
        if color[0] == vazio or color[1] == vazio:
            sensores_cor.Alinhar(rodas, cor=vazio)
            rodas.BackwardForDistance(0.15)
            rodas.Turn()

        elif color[0] == verde or color[1] == verde:
            sensores_cor.Alinhar(rodas)
            rodas.BackwardForDistance(0.15)
            rodas.Turn(180)
                    
        elif color[0] == preto or color[1] == preto:
            sensores_cor.Alinhar(rodas)
            rodas.Stop()
            return

        else: rodas.Forward(speed = 15);
        
    return
        
def MapearColors(robot, timestep, sensores_cor, rodas ):
    
    EncontrarPreto(robot, timestep, sensores_cor, rodas)

    rodas.ForwardForDistance(0.1)
    rodas.Turn()

    Invert = False;
    Ordem = []
    while robot.step(timestep) != -1:
        
        color = sensores_cor.IdentifyColor()
        
        if color[0] == preto: rodas.Turn(-1)
        elif color[1] == preto: rodas.Turn(1)
        
        elif amarelo not in Ordem and color[Invert] == amarelo:
            Ordem.append(amarelo);
        elif vermelho not in Ordem and color[Invert] == vermelho: 
            Ordem.append(vermelho);
        elif azul not in Ordem and color[Invert] == azul: 
            Ordem.append(azul);
        elif color[0] == vazio or color[1] == vazio: 
            if len(Ordem) == 1:
                rodas.BackwardForDistance(0.1)
                rodas.Turn(-180)
                Invert = True
            
            elif len(Ordem) == 2: 
                if amarelo not in Ordem: Ordem.insert(0, amarelo)
                elif vermelho not in Ordem: Ordem.insert(0, vermelho)
                else: Ordem.insert(0, azul)
                rodas.Stop()
                rodas.BackwardForDistance(0.05)
                rodas.Turn(-90)
                return Ordem

        elif len(Ordem) == 2 and Invert:

            if amarelo not in Ordem: Ordem.append(amarelo)
            elif vermelho not in Ordem: Ordem.append(vermelho)
            else: Ordem.append(azul)

            rodas.Stop()
            rodas.BackwardForDistance(0.05)
            rodas.Turn(90)
            rodas.BackwardForDistance(0.03)
            Ordem = list(reversed(Ordem))
            return Ordem

        elif len(Ordem) == 3:
            rodas.Stop()
            rodas.BackwardForDistance(0.05)
            rodas.Turn(-90)
            rodas.BackwardForDistance(0.03)
            return Ordem

        else: rodas.Forward(speed=15);
    return Ordem