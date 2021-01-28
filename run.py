#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import os
import sys
import re
import subprocess

PinForkIn = 12
PinForkOut = 20
PinDialIn = 26
PinDialOut = 21
PinWecker = 17  # Command Pin to turn on/off the relay.
Hits = 10 # How many times should the bell be hit by the hammer?
HitsSleep = 0.06 # Sleep between every hit.
Dialcountdown = 500 # time until to dial the call in ms


GPIO.setmode(GPIO.BCM)
GPIO.setup(PinDialIn,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(PinDialOut,GPIO.OUT)
GPIO.setup(PinForkOut,GPIO.OUT)
GPIO.setup(PinForkIn,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PinWecker, GPIO.OUT)

os.system('/usr/bin/linphonecsh exit')
time.sleep(1)
os.system('/usr/bin/linphonecsh init')
time.sleep(1)
os.system('/usr/bin/linphonecsh soundcard playback')
time.sleep(1)
os.system('/usr/bin/linphonecsh soundcard ring') 
time.sleep(1)
os.system('linphonecsh register --username $(sed -n 1p /boot/sip.txt) --host $(sed -n 2p /boot/sip.txt) --password $(sed -n 3p /boot/sip.txt)')

def wecker():
  for _ in range(Hits):
    GPIO.output(PinWecker, 1)
    time.sleep(HitsSleep)
    GPIO.output(PinWecker, 0)
    time.sleep(HitsSleep)

def hangup():
  FORK = GPIO.input(PinForkIn)
  if FORK == 1:
    os.system('linphonecsh generic terminate')
    time.sleep(0.0001)
  else:
      GPIO.input(PinForkIn)

def answer():
  FORK = GPIO.input(PinForkIn)
  if FORK == 1:
    os.system("linphonecsh generic \"answer $(linphonecsh generic 'calls' | sed -n 4p | awk '{print $1}')\"")
    time.sleep(0.0001)
  else:
      GPIO.input(PinForkIn)

def dialnumber():                 
  DIAL = GPIO.input(PinDialIn)           
  NOM = 0                         
  timeout = False                 
  countdown = 100                 
  while countdown > 0:            
        if timeout:               
          countdown = countdown -1
        if DIAL != 1:             
          if NOM == 0:            
            DIAL = GPIO.input(PinDialIn) 
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
          DIAL = GPIO.input(PinDialIn)   
          countdown = Dialcountdown         
          timeout = True          

def CALL():
  FORK = GPIO.input(PinForkIn)
  time.sleep(0.1)
  if FORK == 1:
    FORK = GPIO.input(PinForkIn)
    time.sleep(0.0001)
    RINGCHECK = 'linphonecsh generic \'calls\' | sed -n 4p | awk \'{print $6}\''
    RINGVALUE = subprocess.check_output(['bash', '-c', RINGCHECK ]).decode().strip()
    if RINGVALUE == 'IncomingReceived':
      wecker()
      FORK = GPIO.input(PinForkIn)
      time.sleep(0.0001)
    else:
      FORK = GPIO.input(PinForkIn)
      time.sleep(0.0001)
  else:
    FORK = GPIO.input(PinForkIn)
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
      FORK = GPIO.input(PinForkIn)
      answer()
    while FORK == 0:
      FORK = GPIO.input(PinForkIn)
      time.sleep(0.001)
    else:
      FORK = GPIO.input(PinForkIn)
      hangup()

while True:
  CALL()
