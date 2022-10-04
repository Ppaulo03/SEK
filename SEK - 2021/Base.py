from Garra import Garra
from Rodas import Rodas
from ColorSensors import ColorSensors

def SetSensor(robot, timestep, name):
    sensor = robot.getDevice(name)
    sensor.enable(timestep)
    return sensor
    
def SetMotor(robot, name):
    wheel = robot.getDevice(name)
    wheel.setPosition(float('inf'))
    wheel.setVelocity(0.0)
    return wheel
    
def DeclararSensoresCor(robot, timestep):
    right = SetSensor(robot, timestep, 'Right_color_sensor')
    left = SetSensor(robot, timestep, 'Left_color_sensor')

    rightDist = SetSensor(robot, timestep, 'distanceColorRight')
    leftDist = SetSensor(robot, timestep, 'distanceColorLeft')

    return [right, left, rightDist, leftDist]

def DeclararSensoresCor(robot, timestep):
    right = SetSensor(robot, timestep, 'Color_Right')
    left = SetSensor(robot, timestep, 'Color_Left')

    right_dist = SetSensor(robot, timestep, 'color_right')
    left_dist = SetSensor(robot, timestep, 'color_left')

    led =  [robot.getDevice('led1'), robot.getDevice('led2')]
    led[0].set(2); led[1].set(2)

    return [right, left, right_dist, left_dist, led]
    
def DeclararSensoresDistancia(robot, timestep):
    lateral_cima = SetSensor(robot, timestep, 'distanciaLadoCima')
    lateral_baixo = SetSensor(robot, timestep, 'distanciaLadoBaixo')
    frontal = SetSensor(robot, timestep, 'distanciaFrente')

    lateral_baixo1 = SetSensor(robot, timestep, 'distanciaLadoBaixo1')
    lateral_baixo2 = SetSensor(robot, timestep, 'distanciaLadoBaixo2')

    return [frontal, lateral_cima, lateral_baixo, lateral_baixo1, lateral_baixo2]
    
def DeclararMotoresRodas(robot, timestep):
    front_left = SetMotor(robot, 'roda1')
    front_right = SetMotor(robot, 'roda2')

    back_left = SetMotor(robot, 'roda3')
    back_right = SetMotor(robot, 'roda4')

    gyro = SetSensor(robot, timestep, 'gyro')
    re = SetSensor(robot, timestep, 're')

    return[front_left, front_right, back_left, back_right, gyro,re]

def DeclararMotoresGarras(robot, timestep):
    base = robot.getDevice('Base Garra')
    base.setPosition(0.0)

    position_sensor = SetSensor(robot, timestep, 'BasePos')
    haste_sensor = SetSensor(robot, timestep, 'PosHaste')

    elevador = robot.getDevice('Elevador Garra')
    elevador.setPosition(0.1)
    
    garra = [robot.getDevice('Garra Out'), robot.getDevice('Garra In')]
    garra[0].setPosition(0.0); garra[1].setPosition(0.0)
    
    haste = robot.getDevice('Haste')
    haste.setPosition(0.095)

    apoio_garra = robot.getDevice('ApoioGarra')
    apoio_garra.setPosition(0)

    return [base, elevador, garra, haste, position_sensor, apoio_garra, haste_sensor]
    
def Declarar(robot, timestep):
    
    sensores_cor = ColorSensors(robot, timestep, DeclararSensoresCor(robot, timestep))
    sensores_distancia = DeclararSensoresDistancia(robot, timestep)
    rodas = Rodas(robot, timestep, DeclararMotoresRodas(robot, timestep))
    garra = Garra(robot, timestep, DeclararMotoresGarras(robot, timestep))

    return [rodas, sensores_distancia, sensores_cor, garra]