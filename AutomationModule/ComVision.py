# -*- coding: utf-8 -*-

import cv2 as cv
from aip import AipOcr
import time


ID = 0 
while(True):
    cap = cv.VideoCapture(ID)
