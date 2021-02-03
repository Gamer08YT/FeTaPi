#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
#import os
#import sys
import re
#import subprocess


GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(6,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

def wecker():
  GPIO.output(17, 1)
  time.sleep(0.08)
  GPIO.output(17, 0)
  time.sleep(0.06)

while True:
  wecker()
