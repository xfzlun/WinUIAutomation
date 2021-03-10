
import cv2 #引入cv库
cap = cv2.VideoCapture(0)  # 创建一个capture实例，这个会返回2个数值，一个布尔值跟一个二进制数组
while True:
    ret, frame = cap.read()  #先用read方法读取cap实例
    cv2.imshow("Video", frame)
#读取内容：
    if cv2.waitKey(10) == ord('q'):  #设定按q退出
        break

#停止调用，关闭窗口

import os
#引入库

print("="*20)
print("=   热键（请在摄像头的窗口使用）：=")
print("= z:更改存储目录     =")
print("= x:拍摄图片        =")
print("= q: 退出        =")
print("="*20)
#提醒用户操作字典

classname = input("请输入存储目录:>>>")
while os.path.exists(classname):
    classname = input("目录已存在！请输存储目录")  #这段逻辑怪怪的，目录已经存在反正是要存储档案用的，已经存在应该没有关系吧
os.mkdir(classname)
#存储

index = 1  # 这个是做啥用的？
cap = cv2.VideoCapture(0)
width = 640
height = 480
w = 360
cap.set(cv2.cap_PROP_FRAME_WIDTH, width)
cap.set(cv2.cap_PROP_FRAME_HEIGHT, height)
crop_w_start = (width-w)//2
crop_h_start = (height-w)//2
print(width, height)
#设置特定值--什么鬼特定值？

while True:
    ret, frame = cap.read()

    frame = frame[crop_h_start:crop_h_start+w, crop_w_start:crop_w_start+w] #这句是做啥用的呢？

    frame = cv2.flip(frame, 1, dst=None)
    #镜像显示
    cv2.imshow("capture", frame)
    #显示

    input = cv2.waitKey(1) & 0xff
    if input == ord('z'):
        class_name = input('请输入存储目录：>>>')
        while os.path.exists(classname):
            class_name = input("目录已存在！请输入存储目录：")
        os.mkdir(classname)
    #存储

    elif input == ord('x'):
        #下面这段可以用来作截图存档的方式，设一个index, 加上今天日期，依次存档
        cv2.imwrite("%s/%d.jpeg" % (classname, index), cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)) 
        print("%s: %d 张图片" % (classname, index))
    
    if input == ord('q'):
        break
    #退出
cap.release()
cv2.destroyAllWindows()