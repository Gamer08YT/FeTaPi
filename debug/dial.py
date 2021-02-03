#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import os
import sys
import re
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(6,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(20,GPIO.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

def dialnumber():                 
  DIAL = GPIO.input(26)           
  NOM = 0                         
  timeout = False                 
  countdown = 100                 
  while countdown > 0:            
        if timeout:               
          countdown = countdown -1
        if DIAL != 1:             
          if NOM == 0:            
            DIAL = GPIO.input(26) 
          else:                   
            if NOM == 10:         
              print("0", end='')
            else:                 
              print(NOM, end='')
          NOM = 0                 
          time.sleep(0.01)        
        elif DIAL == 1:           
          NOM = NOM +1            
          time.sleep(0.109)       
          DIAL = GPIO.input(26)   
          countdown = 300         
          timeout = True          

def CALL():
      orig_stdout = sys.stdout
      f = open('dial.txt', 'w')
      sys.stdout = f
      dialnumber()
      time.sleep(0.0001)
      sys.stdout = orig_stdout
      f.close()
      os.system('cat dial.txt')

while True:
  CALL()
