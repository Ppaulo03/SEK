#!/usr/bin/env python3
import os

path = "/home/robot/Teste/Logs"
dir = os.listdir(path)
for file in dir:
    if file !="clear_logs.py":
        os.remove(file)