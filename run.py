#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import os
import sys
import re
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(6,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(20,GPIO.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

os.system('linphonecsh exit')
time.sleep(1)
os.system('linphonecsh init')
time.sleep(1)
os.system('linphonecsh soundcard playback')
time.sleep(1)
os.system('linphonecsh soundcard ring') 
time.sleep(1)
os.system('linphonecsh register --username <Nummer> --host hg.eventphone.de --password <password>')

def wecker():
  GPIO.output(17, 1)
  time.sleep(0.04)
  GPIO.output(17, 0)
  time.sleep(0.04)
  GPIO.output(17, 1)
  time.sleep(0.04)
  GPIO.output(17, 0)
  time.sleep(0.04)
  GPIO.output(17, 1)
  time.sleep(0.04)
  GPIO.output(17, 0)
  time.sleep(0.04)
  GPIO.output(17, 1)
  time.sleep(0.04)
  GPIO.output(17, 0)
  time.sleep(0.04)
  GPIO.output(17, 1)
  time.sleep(0.04)
  GPIO.output(17, 0)
  time.sleep(0.04)
  GPIO.output(17, 1)
  time.sleep(0.04)
  GPIO.output(17, 0)
  time.sleep(0.04)
  GPIO.output(17, 1)
  time.sleep(0.04)
  GPIO.output(17, 0)
  time.sleep(0.04)
  GPIO.output(17, 1)
  time.sleep(0.04)
  GPIO.output(17, 0)
  time.sleep(0.04)


def hangup():
  FORK = GPIO.input(6)
  if FORK == 1:
    os.system('linphonecsh generic terminate')
    time.sleep(0.0001)
  else:
      GPIO.input(6)

def answer():
  FORK = GPIO.input(6)
  if FORK == 1:
    os.system("linphonecsh generic \"answer $(linphonecsh generic 'calls' | sed -n 4p | awk '{print $1}')\"")
    time.sleep(0.0001)
  else:
      GPIO.input(6)

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
          countdown = 500         
          timeout = True          

def CALL():
  FORK = GPIO.input(6)
  time.sleep(0.1)
  if FORK == 1:
    FORK = GPIO.input(6)
    time.sleep(0.0001)
    RINGCHECK = 'linphonecsh generic \'calls\' | sed -n 4p | awk \'{print $5}\''
    RINGVALUE = subprocess.check_output(['bash', '-c', RINGCHECK ]).decode().strip()
    if RINGVALUE == 'IncomingReceived':
      wecker()
      FORK = GPIO.input(6)
      time.sleep(0.0001)
    else:
      FORK = GPIO.input(6)
      time.sleep(0.0001)
  else:
    FORK = GPIO.input(6)
    CMD = 'linphonecsh generic "answer $(linphonecsh generic \'calls\' | sed -n 4p | awk \'{print $1}\')"'
    VALUE = subprocess.check_output(['bash', '-c', CMD ]).decode().strip()
    if VALUE == 'There are no calls to answer.':
      orig_stdout = sys.stdout
      f = open('dial.txt', 'w')
      sys.stdout = f
      dialnumber()
      time.sleep(0.0001)
      sys.stdout = orig_stdout
      f.close()
      os.system('linphonecsh dial $(cat dial.txt)')
    else:
      FORK = GPIO.input(6)
      answer()
    while FORK == 0:
      FORK = GPIO.input(6)
      time.sleep(0.001)
    else:
      FORK = GPIO.input(6)
      hangup()

while True:
  CALL()
