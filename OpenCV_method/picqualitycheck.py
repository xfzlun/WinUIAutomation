# -*- coding: utf-8 -*-

'''
提高OCR识别率， 如果遇到图像质量差的二值图返回不识别，只识别质量高一点的二值图，灰度图，以及RGB图
利用'白底方差'，图像方差，像素波动方差，图像大小/分辨率 这4个参考因素
质量差的条件：如果像素波动方差小于1，图像大小/分辨率 小于0.01， 则属于质量差的图片

'''
import cv2
import os
import csv
import numpy as np

#这个函数的目的应该是取得图像档案的位置
def get_img(Img_path):  
    image_paths = []
    for (dir, dirnames, filenames) in os.walk(Img_path):   #os.walk()这是啥意思啊？
        for img_file in filenames:
            ext = ['.jpg', '.png', 'jpeg', '.tif']
            if img_file.endswith(tuple(ext())):  #endswith()啥意思？
                image_paths.append(dir+'/'+img_file)
    return image_paths

#计算图片的品质
def Calculate_QD(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 对于取得的图像进行灰度处理

    numdiff = np.diff(gray)
    var_all = np.sum((numdiff) ** 2) / gray.size

    baseline = np.bincount(gray.reshape(1, -1)[0])  # 用途？
    sortNum = np.argsort(baseline)
    var_255 = np.sum((gray - sortNum[-1]) ** 2) / gray.size
    var_000 = np.sum((gray - sortNum[-2]) ** 2) / gray.size
    return var_255, var_000, var_all

if __name__ == '__main__':
    Img_path = './idcard'
    csv_path = './idcard.csv'
    Imgpaths = get_img(Img_path)
    Result_csv = []

    for Img_path in Imgpaths:
        filename = Img_path.split('/')[-1]
        imgArray = cv2.imread(Img_path)
        image_size = os.path.getsize(Img_path)
        px_size = round(image_size/imgArray.size),4)
        var_255, var_000, var_all = Calculate_QD(imgArray)
        Result_csv.append((filename, var_255, var_000, var_all, px_size))
    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerrow(('filename', '白底方差', '图像方差', '像素波动方差', '图像大小/分辨率'))
        csv_writer.writerows(Result_csv)
        
