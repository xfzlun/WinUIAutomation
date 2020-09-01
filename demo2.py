#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 15:38
# @Author  : lillian
# @File    : xmp.py
import cv2 as cv
from aip import AipOcr
import numpy as np
import os
import paramiko
import time
import warnings
from openpyxl import Workbook


""" 初 始 化 部 分 """
#APP_ID = '18044023'
#API_KEY = 'xdMedP6gkH2X6hZbUAfnqvr0'
#SECRET_KEY = 'igeVigIi65Np9Vv0K6yL0U2mTpkyhdsd'
warnings.filterwarnings("ignore")

with open(r'F:\0testexe\FBIOS\V3.01/ipconfig.txt') as f:
#with open('./ipconfig.txt') as f:
    text = f.read()
    name = text.split('\n')
    workingdir = name[2].split('=')
    app_id = name[3].split('=')
    app_key = name[4].split('=')
    secret_key = name[5].split('=')
    bmcip = name[1].split('=')

APP_ID = app_id[1]
API_KEY = app_key[1]
SECRET_KEY = secret_key[1]
#连接百度API端口
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
BMC_IP = bmcip[1]
# 实例化一个transport对象
transport = paramiko.Transport((BMC_IP, 22))
# 建立连接
transport.connect(username='sysadmin', password='superuser')
# 将sshclient的对象的transport指定为以上的transport
ssh = paramiko.SSHClient()
ssh._transport = transport
ID = 0

def usbCamDetect():
    ID = 0
    global cap
    cap = cv.VideoCapture(ID)
    while(ID < 4):
        if cap.isOpened():
            print(ID)
            cap.release()
            return ID
        else:
            print('id %d has no cam detected...' % ID)
            ID += 1
    cap.release()

usbCamDetect()

"""截取指定位置的图片"""
def video_select_size(a,b,c,d):
    capture = cv.VideoCapture(ID + cv.CAP_DSHOW)  # 读取当前USB摄像头
    #capture = cv.VideoCapture(ID)
    capture.set(3, 1280)
    capture.set(4, 720)
    alltext=[]
    i = 0
    while (True):
        ret, frame = capture.read()  # 读取当前视频画面的信息，frame是每一帧的图像
        capture.release()
        # print(frame)
        try:
            if frame == None:
                print('No connect video')
                break
        except ValueError:
            sp = frame.shape
            newpic = frame[a:b,c:d]
            cv.imwrite('./result.bmp',newpic)
            image = get_file_content('./result.bmp')
            results = client.basicGeneral(image)["words_result"]
            for result in results:
                alltext.append(result["words"])
        break
    return alltext

"""截取所选栏位"""
def select_place(image):
    #image = 'result3.bmp'
    files = os.listdir('./mark')
    for file in files:
        path = './mark'+'/'+file
        os.remove(path)
    savefile = './mark'

    picture = []
    # 设定颜色HSV范围，假定为红色
    #redLower = np.array([0, 60, 46])
    #redUpper = np.array([5, 255, 255])

    # 读取图像
    #img = cv.imread(image)
    img = image

    # 将图像转化为HSV格式
    #hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # 去除颜色范围外的其余颜色
    #mask = cv.inRange(hsv, redLower, redUpper)
    #二值化操作，灰度
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 26, 255, cv.THRESH_BINARY)
    # 二值化操作
    #ret, binary = cv.threshold(mask, 0, 255, cv.THRESH_BINARY)

    # 膨胀操作，因为是对线条进行提取定位，所以腐蚀可能会造成更大间隔的断点，将线条切断，因此仅做膨胀操作
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv.dilate(binary, kernel, iterations=1)
    #cv.imwrite('3.jpg', img)
    # 获取图像轮廓坐标，其中contours为坐标值，此处只检测外形轮廓
    a, contours, hierarchy = cv.findContours(dilation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # cv2.boundingRect()返回轮廓矩阵的坐标值，四个值为x, y, w, h， 其中x, y为左上角坐标，w,h为矩阵的宽和
        boxes = [cv.boundingRect(c) for c in contours]
        for box in boxes:
            x, y, w, h = box
            save_image = os.path.join(savefile, str(x)+'_'+str(y)+'_'+str(w)+'_'+str(h) + '.jpg')
            # 绘制矩形框对轮廓进行定位
            # cv2.rectangle(img, (x, y), (x+w, y+h), (153, 153, 0), 2)
            # 将绘制的图像保存并展示
            if (w > 800) and (10<y<600) and (10<h<40) and (x<10):
                new = img[y:y + h, x:x + w]
                cv.imwrite(save_image, new)
    return

def select_place2(image):
    #image = 'result3.bmp'
    files = os.listdir('./mark')
    for file in files:
        path = './mark'+'/'+file
        os.remove(path)
    savefile = './mark'

    picture = []
    # 设定颜色HSV范围，假定为红色
    #redLower = np.array([0, 60, 46])
    #redUpper = np.array([5, 255, 255])

    # 读取图像
    #img = cv.imread(image)
    img = image

    # 将图像转化为HSV格式
    #hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # 去除颜色范围外的其余颜色
    #mask = cv.inRange(hsv, redLower, redUpper)
    #二值化操作，灰度
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 26, 255, cv.THRESH_BINARY)
    # 二值化操作
    #ret, binary = cv.threshold(mask, 0, 255, cv.THRESH_BINARY)

    # 膨胀操作，因为是对线条进行提取定位，所以腐蚀可能会造成更大间隔的断点，将线条切断，因此仅做膨胀操作
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv.dilate(binary, kernel, iterations=1)
    #cv.imwrite('3.jpg', img)
    # 获取图像轮廓坐标，其中contours为坐标值，此处只检测外形轮廓
    a, contours, hierarchy = cv.findContours(dilation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # cv2.boundingRect()返回轮廓矩阵的坐标值，四个值为x, y, w, h， 其中x, y为左上角坐标，w,h为矩阵的宽和
        boxes = [cv.boundingRect(c) for c in contours]
        for box in boxes:
            x, y, w, h = box
            save_image = os.path.join(savefile, str(x)+'_'+str(y)+'_'+str(w)+'_'+str(h) + '.jpg')
            # 绘制矩形框对轮廓进行定位
            # cv2.rectangle(img, (x, y), (x+w, y+h), (153, 153, 0), 2)
            # 将绘制的图像保存并展示
            if (w > 400) and (10<y<600) and (10<h<40) and (x<10):
                new = img[y:y + h, x:x + w]
                cv.imwrite(save_image, new)
    return

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def video_bios_select(): #视频显示
    #capture1 = cv.VideoCapture(ID+cv.CAP_DSHOW)# 读取当前USB摄像头
    #capture1 = cv.VideoCapture(ID)
    #print(cv.CAP_DSHOW)
    cap.release()
    cap.open(ID)
    cap.set(3,1280)
    cap.set(4,720)
    global videoFlag
    videoFlag = cap.isOpened()
    while (videoFlag):
        ret,frame = cap.read()#读取当前视频画面的信息，frame是每一帧的图像
        try:
            if ret:
                print('saving pic.....')
                newpic = frame[0:720, 0:500]
                select_place2(newpic)
                if os.listdir(r'./mark'):
                    print('select mode,please wait')
                    filenames = os.listdir(r'./mark')
                    """ 调用通用文字识别, 图片参数为本地图片 """
                    if filenames:
                        for n in filenames:
                            path = './mark' + '/' + n
                            image = get_file_content(path)
                            results = client.basicGeneral(image)["words_result"]  # 还可以使用身份证驾驶证模板，直接得到字典对应所需字段
                            sp = []
                        for result in results:
                            sp.append(result["words"])
                else:
                    print('no select mode,please wait')
                    name = './result.bmp'
                    cv.imwrite(name, frame)
                    image = get_file_content(name)
                    results = client.basicGeneral(image)["words_result"]
                    sptext = []
                    for result in results:
                        sptext.append(result["words"])
                break
            else:
                print('No Image....')
                break
        except IOError:
            print("Pic can not be saved")
            break
        cap.release()
    return sptext

def video_demo(): #视频显示
    if ID != None:
        print('Screen Capturing>>>')
        #global cap
        #cap = cv2.VideoCapture(usbid)
        #codec = 0x47504A4D  # MJPG
        #cap.set(cv.CAP_PROP_FPS, 30.0)
        #cap.set(cv.CAP_PROP_FOURCC, codec)
        cap.open(ID)
        cap.set(3,1280)#1024
        cap.set(4,720)#768
        print('Image reading>>>')
        #ret, frame = cap.read()
        global videoFlag
        print('Camera detecting...')
        videoFlag = cap.isOpened()
        while (videoFlag):
            #cv2.waitKey(1)
            ret, frame = cap.read()
            try:
                if ret:
                    print('saving pic.....')
                    select_place(frame)
                    if os.listdir(r'./mark'):
                        print('select mode,please wait')
                        filenames = os.listdir(r'./mark')
                        """ 调用通用文字识别, 图片参数为本地图片 """
                        if filenames:
                            for n in filenames:
                                path = './mark' + '/' + n
                                image = get_file_content(path)
                                results = client.basicGeneral(image)["words_result"]  # 还可以使用身份证驾驶证模板，直接得到字典对应所需字段
                                sptext = []
                            for result in results:
                                sptext.append(result["words"])
                    else:
                        cap.release()
                        sptext = video_bios_select()
                    break
                else:
                    print('No Image....')
                    break
            except IOError:
                print("Pic can not be saved")
                break
    else:
        print('No Camera detected!')
    print('Camera closing>>>')
    cap.release()
    return sptext

def video_all(): #视频显示
    capture = cv.VideoCapture(ID+cv.CAP_DSHOW)# 读取当前USB摄像头
    #capture = cv.VideoCapture(ID)
    capture.set(3,1280)#1024
    capture.set(4,720)#768
    i=0
    while(True):
        ret,frame = capture.read()#读取当前视频画面的信息，frame是每一帧的图像
        capture.release()
        #print(frame)
        try:
            if frame == None:
                print('No connect video')
                break
        except ValueError:
            #frame = cv.flip(frame,1) #图像镜像变化
            #cv.imshow("video",frame)
            #name = './result'+str(i)+'.bmp'
            #cv.imwrite(name, frame)
            #fname = './result.bmp'
            #print(frame.shape)
            #image = get_file_content(name)
            name = './result.bmp'
            cv.imwrite(name, frame)
            image = get_file_content(name)
            results = client.basicGeneral(image)["words_result"]
            alltext=[]
            for result in results:
                alltext.append(result["words"])
            #img = cv.imread(fname)
            #name2 = './'+str(i)+'.txt'
            #f1 = open(name2,'w')
            #for result in results:
            #    text = result["words"]
             #   f1.write(text)
            #i+=1
            #if c == 27: # 按ESC退出
            return alltext
        break

#高精度识别，一天500次
def video_high_ocr():
    capture = cv.VideoCapture(ID + cv.CAP_DSHOW)  # 读取当前USB摄像头
    #capture = cv.VideoCapture(ID)
    capture.set(3, 1280)
    capture.set(4, 720)
    i = 0
    while (True):
        ret, frame = capture.read()  # 读取当前视频画面的信息，frame是每一帧的图像
        capture.release()
        # print(frame)
        try:
            if frame == None:
                print('No connect video')
                break
        except ValueError:
            name = './result.bmp'
            cv.imwrite(name, frame)
            image = get_file_content(name)
            results = client.basicAccurate(image)["words_result"]
            alltext = []
            for result in results:
                alltext.append(result["words"])
            return alltext
        break

def high_ocr(picture):
    image = get_file_content(picture)
    results = client.basicAccurate(image)["words_result"]
    alltext = []
    for result in results:
        alltext.append(result["words"])
    return alltext

def check_post(text):
    sta='post'
    stdin, stdout, stderr = ssh.exec_command('usb_enable')
    print(text)
    for i in text:
        if 'installed' in i:
            print('New CPU installed,Press F1 to Run SETUP')
            sta = 'newcpu'
        elif 'fail' in i:
            print('DOCP or XMP fail')
            sta = 'docpfail'
        elif 'recover' in i:
            print('flash bios,press F1 to run setup')
            sta = 'newbios'
        elif 'over' in i:
            print(' hardware monitor error ')
            sta = 'tempover'

    return sta


##x_start,x_end,y_start,y_end
#print(text)
#pic_to_file(r'F:\0testexe\opencv\TUF Z370-PLUS GAMING_2401\EZMODE\fast',100,550,0,1000)
#b=video_select_size(100,550,0,1000)
a=video_demo()
print(a)
#stdin, stdout, stderr = ssh.exec_command('usb_enable')
#enter_bios(stdin, stdout, stderr)
#select_onoff('off')
