import math

class ColorSensors:

    vermelho = [201, 44, 52]; 
    branco = [210, 211, 214]; 
    amarelo = [210, 204, 32]; 
    verde = [[30, 217, 33], [28, 199, 30]]; # Pista com 2 diferentes verdes
    azul = [29, 30, 214]; 
    preto = [29, 30, 32]; 
    vazio = [34, 34, 34] #Teste empírico
    ledCor = False;

    def __init__(self, robot, timestep, sensores):
        self.robot = robot
        self.timestep = timestep
        self.right = sensores[0]
        self.left = sensores[1]
        self.right_dist = sensores[2]
        self.left_dist = sensores[3]
        self.led = sensores[4]
    
    def GetColor(self, sensor, dist):

        if dist.getValue() >= 1000: return 0 #Vazio
        image = sensor.getImageArray()
        if image:
            red = 0; green = 0; blue = 0; count = 0;
            for x in range(0, sensor.getWidth()):
                for y in range(0, sensor.getHeight()):
                    red   += image[x][y][0]
                    green += image[x][y][1]
                    blue  += image[x][y][2]
                    count += 1
            red=red/count; green=green/count; blue=blue/count
            color = [red, green, blue]
            
            if   color == self.vermelho: return 1 #Vermelho
            elif color == self.branco: return 2 #Branco
            elif color == self.amarelo: return 3 #Amarelo
            elif color in self.verde: return 4 #Verde
            elif color == self.azul: return 5 #Azul
            elif color == self.preto: return 6 #Preto
            else: return 10
        else: return 10

    def IdentifyColor(self):
        right_color = self.GetColor(self.right, self.right_dist)
        left_color =  self.GetColor(self.left, self.left_dist)
        return [right_color, left_color]

    def PiscarLed(self):
        self.ledCor = not self.ledCor
        self.led[0].set(self.ledCor); self.led[1].set(self.ledCor)
    
    def DesligarLed(self):
        self.led[0].set(2); self.led[1].set(2)


    def Alinhar(self, rodas, cor = 2, angle = 5, turnSpeed = 5, speed = 1):
        if cor == 0: speed = - speed; angle = -angle

        self.PiscarLed()
        while self.robot.step(self.timestep) != -1:
            color = self.IdentifyColor()
            if color[0] != cor and color[1] != cor: rodas.Backward(speed = speed)
            else: break
            self.PiscarLed()

        cont = 0
        while self.robot.step(self.timestep) != -1:
            cont += 1
            if cont == 20: angle = angle/5; turnSpeed = turnSpeed/2.5;
            elif cont == 30: self.DesligarLed(); return
            
            color = self.IdentifyColor();
            if color[0] == cor and color[1] == cor:

                while self.robot.step(self.timestep) != -1:
                    color = self.IdentifyColor();
                    if color[0] == cor and color[1] == cor: rodas.Forward(speed = speed)

                    elif (color[0] != cor and color[1] != cor):
                        rodas.Stop();
                        self.DesligarLed()
                        return

                    elif (color[0] != cor and color[1] == 10) or (color[1] != cor and color[0] == 10):
                        rodas.Stop();
                        self.DesligarLed()
                        return

                    else: break
                    self.PiscarLed()

            elif color[0] != cor and color[1] != cor:
                
                while self.robot.step(self.timestep) != -1:
                    color = self.IdentifyColor();
                    if color[0] != cor and color[1] != cor: rodas.Backward(speed = speed)
                    elif color[0] == cor and color[1] == cor: 
                        rodas.Stop();
                        self.DesligarLed()
                        return
                    elif (color[0] == cor and color[1] == 10) or (color[1] == cor and color[0] == 10):
                        rodas.Stop();
                        self.DesligarLed()
                        return
                    else: break
                    self.PiscarLed()

            color = self.IdentifyColor()
            if color[0] == cor: rodas.Turn(angle, speed = turnSpeed, alinhando= True)
            else: rodas.Turn(-angle, speed = turnSpeed, alinhando= True);
            self.PiscarLed()