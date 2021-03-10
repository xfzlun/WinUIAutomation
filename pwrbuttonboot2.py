# -*- CODING: UTF-8 -*-
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)  # 设定Board编号方式，基于BCM编号;还有另外一个BOARD引脚编号
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)
time.sleep(1)
GPIO.cleanup(17)

# 把这个写成一个函数或是class

#while True:
    #GPIO.output(17, GPIO.HIGH)
    #time.sleep(1)
    #GPIO.output(17, GPIO.LOW)
    #time.sleep(1)
