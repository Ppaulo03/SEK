from controller import Robot
from Base import Declarar
from PickCano import PegarCano
from MapColors import MapearColors
from Gasoduto import DoGasoduto
from AcharCor import AcharCor

#Declarações do Robo
timestep = 32
robot = Robot()

p = 0.1; m = 0.15; g = 0.20;
sequencia_base = [m,p,g]
sequencia = []

[rodas, sensores_distancia, sensores_cor, garra] = Declarar(robot, timestep)
rodas.ForwardForDistance(0.2, speed=0) #Equivalente a um Sleep

ordem = MapearColors(robot, timestep, sensores_cor, rodas )
while robot.step(timestep) != -1:
    

    if len(sequencia_base) == 0: break
    if len(sequencia) == 0:
        tmp = sequencia_base.pop(0)
        sequencia.append(tmp)
        sequencia_base.append(tmp)

    '''if g in sequencia: size = g
    elif m in sequencia: size = m
    else: size = p'''
    size = sequencia[0]

    AcharCor(robot, timestep, sensores_cor, rodas, size, ordem)
    if not PegarCano(robot, timestep, size, sensores_distancia,sensores_cor, rodas, garra): 
        if size in sequencia_base: sequencia_base.remove(size)
        if size in sequencia: sequencia.remove(size)
    else:
        [colocado, sequencia] = DoGasoduto(robot, timestep, sensores_distancia, rodas, sensores_cor,size, garra, sequencia_base)
        if not colocado:
            AcharCor(robot, timestep, sensores_cor, rodas, size, ordem)
            
            #Devolve o cano para a area dele
            rodas.ForwardForDistance(0.3)
            rodas.Turn(90)
            rodas.ForwardForDistance(0.1)
            garra.Tras()
            garra.Girar(90)
            garra.Descer()
            garra.Abrir()
            garra.Subir()
            garra.Girar(-90)
            garra.Fechar()
            garra.Frente()
            rodas.BackwardForDistance(0.1)
            
            for v in sequencia_base:
                if v not in sequencia: sequencia_base.remove(v)
        if len(sequencia) == 0: break