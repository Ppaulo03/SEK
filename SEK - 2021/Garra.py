import math
class Garra:

    elevator_height = 0.1; haste_size = 0.095; garra_angle = math.radians(85)
    
    def __init__(self, robot, timestep, motores):  
        self.robot = robot
        self.timestep = timestep
        self.base = motores[0]
        self.angle = 0
        self.elevador = motores[1]
        self.garra = motores[2]
        self.haste = motores[3]
        self.base_position_sens = motores[4]
        self.apoio_garra = motores[5]
        self.haste_sensor = motores[6]


    def Wait(self, time):
        end_time = self.robot.getTime() + time

        while self.robot.step(self.timestep) != -1:
            current_time = self.robot.getTime()
            if current_time >= end_time: return

    def Frente(self, heigh = haste_size):
        self.haste.setPosition(heigh)
        self.Wait(1)
    
    def Tras(self, heigh = 0.0):
        self.haste.setPosition(heigh)
        self.Wait(1)
        
    def Subir(self, heigh = elevator_height):
        self.elevador.setPosition(heigh)
        self.Wait(1)

    def Descer(self, heigh = 0.0):
        self.elevador.setPosition(heigh)
        self.Wait(1)
            
    def Girar(self, angle):
        angle = math.radians(angle)
        self.angle = self.angle + angle
        self.base.setPosition(self.angle)
        while self.robot.step(self.timestep) != -1:
            pos = self.base_position_sens.getValue()
            if pos >= self.angle - 0.01 and pos <= self.angle + 0.01: break
    
    def GirarReset(self):
        self.angle = 0
        self.base.setPosition(self.angle)
        while self.robot.step(self.timestep) != -1:
            pos = self.base_position_sens.getValue()
            if pos >= self.angle - 0.01 and pos <= self.angle + 0.01: break
               
    def Abrir(self):
        self.garra[0].setPosition(-self.garra_angle)
        self.garra[1].setPosition(self.garra_angle)
        self.Wait(1)
            
    def Fechar(self):     
        self.garra[0].setPosition(0.0)
        self.garra[1].setPosition(0.0)
        self.Wait(1)
    
    def GirarApoioGarra(self, angle):
        self.apoio_garra.setPosition(math.radians(angle))
        self.Wait(1)