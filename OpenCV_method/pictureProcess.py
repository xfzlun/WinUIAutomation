import cv2
import os
import time
import numpy as np
import matplotlib.pyplot as pyplot

picPath = '~/Documents/result.png'  #先标明目前工作目录
fullPath = os.path.expanduser(picPath)  #
print(fullPath)
cap = cv2.imread(fullPath)



