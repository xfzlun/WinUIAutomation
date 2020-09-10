# 【Python】提取图像中的主要颜色
import cv2
import numpy as np
from PIL import Image
 
 
img_path = './images/origin_image.jpg'
image = Image.open(img_path)
 
# 要提取的主要颜色数量
num_colors = 5
 
small_image = image.resize((80, 80))
result = small_image.convert('P', palette=Image.ADAPTIVE, colors=num_colors)   # image with 5 dominating colors
 
result = result.convert('RGB')
# result.show() # 显示图像
main_colors = result.getcolors(80*80)
# print(main_colors)
 
# 显示提取的主要颜色
for count, col in main_colors:
    if count < 40:
        continue
    a = np.zeros((224,224,3))
    a = a + np.array(col)
    # print(a)
    cv2.imshow('a',a.astype(np.uint8)[:,:,::-1])
    cv2.waitKey()
