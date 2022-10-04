import math
class Rodas:

    wheel_radius = 0.025
    distance_between_wheels = 0.185
    turn_speed =  2
    forward_speed = 10
    Cano = False
    
    def __init__(self, robot, timestep, motores):  
        self.robot = robot
        self.timestep = timestep
        self.front_left = motores[0]
        self.front_right = motores[1]
        self.back_left = motores[2]
        self.back_right = motores[3]
        self.gyro = motores[4]
        self.gyro.disable()
        self.re = motores[5]

    def Stop(self):
        self.front_left.setVelocity(0.0)
        self.front_right.setVelocity(0.0)
        self.back_left.setVelocity(0.0)
        self.back_right.setVelocity(0.0)
        
    def Forward(self, speed = forward_speed):
        self.front_left.setVelocity(speed)
        self.front_right.setVelocity(speed)
        self.back_left.setVelocity(speed)
        self.back_right.setVelocity(speed)

    def ForwardForDistance(self, distance, speed = forward_speed, pos_sensor = None):
        if speed != 0: linear_velocity_forward = speed * self.wheel_radius
        else: linear_velocity_forward = self.forward_speed * self.wheel_radius

        duration = distance / linear_velocity_forward 
        end_time = self.robot.getTime() + duration

        if pos_sensor is not None: pos = pos_sensor.getValue()
        else: pos = 0;

        while self.robot.step(self.timestep) != -1:
            current_time = self.robot.getTime()
            if pos_sensor is not None:
                if pos_sensor.getValue() > pos + 0.005: return False
         
            if current_time > end_time:
                self.Stop()
                return True
            else:
                self.Forward(speed)

    def Backward(self, speed = forward_speed):
        self.front_left.setVelocity(-speed)
        self.front_right.setVelocity(-speed)
        self.back_left.setVelocity(-speed)
        self.back_right.setVelocity(-speed)

    def BackwardForDistance(self, distance, speed = forward_speed):
        if speed != 0: linear_velocity_forward = speed * self.wheel_radius
        else: linear_velocity_forward = self.forward_speed * self.wheel_radius
        beggining = self.robot.getTime()
        duration = distance / linear_velocity_forward 
        end_time = beggining + duration 
        
        while self.robot.step(self.timestep) != -1:
            current_time = self.robot.getTime()
            
            if current_time > end_time:
                self.Stop()
                return True
            elif self.re.getValue() >= 1000: self.Stop(); return False
            else:
                self.Backward(speed)
     
    def Turn(self, angle = 90, speed = turn_speed, alinhando = False, recursiv = False):
        angle = math.radians(angle)
        if speed != 0: rate_of_rotation = (2*self.wheel_radius*speed)/self.distance_between_wheels
        else: rate_of_rotation = (2*self.wheel_radius*self.turn_speed)/self.distance_between_wheels
        pos = 1
        if(angle < 0):
            angle = -angle
            speed = -speed
            pos = -1
        
        end_time = self.robot.getTime() + (angle/rate_of_rotation)

        self.gyro.enable(self.timestep)
        cont = 0; soma = 0;

        beggining = self.robot.getTime()
        while self.robot.step(self.timestep) != -1:
            soma += self.gyro.getValues()[1]; cont += 1
            current_time = self.robot.getTime()
            if current_time < end_time:
                self.front_left.setVelocity(-speed)
                self.front_right.setVelocity(speed)
                self.back_left.setVelocity(-speed)
                self.back_right.setVelocity(speed)
            else:
                self.Stop()
                self.gyro.disable()
                if alinhando: break
                
                girado = (soma/cont) * (self.robot.getTime() - beggining)
                diff = math.degrees(angle - abs(girado))
                if abs(diff) >= 0.5:
                    if diff > 10: sp = 10
                    else: sp = abs(diff)
                    self.Turn(pos*diff, speed= sp, recursiv=True)
                break

    def GetDistance(self, time, speed = forward_speed):
        return time * speed * self.wheel_radius