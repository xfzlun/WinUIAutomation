# -*- coding:utf-8 -*-

import cv2
img =cv2.imread("./result.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 15, 255,cv2.THRESH_BINARY)
img_binary = cv2.imwrite('./result_binary2.png', binary)
contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img,contours,-1,(0,0,255),3)

cv2.imwrite("img_draw.png", img)
print(len(contours))
print(contours)
