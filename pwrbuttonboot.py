# -*- CODING: UTF-8 -*-
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)  # 设定Board编号方式，基于BCM编号
GPIO.setwarnings(False) #  如果RPi.GPIO检测到引脚已被配置为默认（输入）以外的其他引脚，则在尝试配置脚本时会收到警告。要禁用这些警告
GPIO.setup(17, GPIO.OUT)  #  设置GPIO引脚为输出状态
GPIO.output(17, GPIO.LOW)  # 设置GPIO输出低电平
time.sleep(1)  # 维持低电平1秒
GPIO.cleanup(17)  # GPIO 17恢复默认

'''
#反复点亮LED
while True:
    GPIO.output(17, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(17, GPIO.LOW)
    time.sleep(1)
'''