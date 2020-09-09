import cv2
import os
import time
import numpy as np
import matplotlib.pyplot as pyplot

picPath = '~/Documents/result.png'  #标明图片档案所在位置
fullPath = os.path.expanduser(picPath)  #
print(fullPath)
cap = cv2.imread(fullPath)



