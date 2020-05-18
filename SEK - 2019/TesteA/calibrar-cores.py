#!/usr/bin/env python3
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor, ColorSensor, UltrasonicSensor
from time import sleep
from ev3dev2.sound import Sound

ent_sc_esq = INPUT_1
ent_sc_dir = INPUT_2
#ent_us_lat = INPUT_3
#ent_us_fr = INPUT_4
cor_esq = ColorSensor(ent_sc_esq)
cor_dir = ColorSensor(ent_sc_dir)
#us_lat = UltrasonicSensor(ent_us_lat)
#us_fr = UltrasonicSensor(ent_us_fr)
a=0
sound = Sound()


cor_esq.mode = 'RGB-RAW'
cor_dir.mode = 'RGB-RAW'

def qual_cor(sensor):
    cores = {'e':[27,199,114],
             'd':[23,150,64]}
    re = cor_esq.red
    rd = cor_dir.red
    ge = cor_esq.green
    gd = cor_dir.green
    be = cor_esq.blue
    bd = cor_dir.blue
    ne = [re,ge,be]
    nd = [rd,gd,bd]
    i = 0
    if sensor='d':
        n=nd
    else:
        n=ne
    while i < 3:
        v = n[i]
        li = cores[sensor][i] - 20
            ls = cores[sensor][i] + 20
            if li <= v <= ls:
                score += 1
            i = i+1
        if score >=2:
            cor_vista = 3
    return cor_vista

