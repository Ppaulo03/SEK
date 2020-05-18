from Alinhamento_inicial import alinhamento_meeting_area
from Aprender_cores import aprender_cores
from Achar_cor import achar_cor
from Pegar_Cano import pegar_cano
from time import sleep
from Robô import Robot

Kleiton = Robot()
while True:
    if Kleiton.btn().any():
        Kleiton.sound().beep() 
        break
    else:
        sleep(0.01)

Kleiton.set_rgbmax()

while True:
    alinhamento_meeting_area(Kleiton)
    aprender_cores(Kleiton)
    achar_cor(Kleiton)
    pegar_cano(Kleiton)
    