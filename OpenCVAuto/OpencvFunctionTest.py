# 以下代码可用来测试OpenCV摄像头功能
# 有一个问题，就是这个方式调用不了MAC Book的相机，还在研究怎么解决

import cv2 #引入cv库
#测试相机使用那个代号
cam_test = 10
for i in range(0, cam_test):
    cap = cv2.VideoCapture(i)
    test, frame = cap.read()
    print("i:"+str(i)+" /// result:" + str(test))

cap = cv2.VideoCapture(0)  # 创建一个capture实例，这个会返回2个数值，一个布尔值跟一个二进制数组
while True:
    ret, frame = cap.read()  #先用read方法读取cap实例
    cv2.imshow("Video", frame)
#显示图像cv2.imshow()
#使用函数cv2.imshow() 显示图像。窗口会自动调整为图像大小。第一个参数是窗口的名字，其次才是我们的图像。你可以创建多个窗口，只要你喜欢，但是必须给他们不同的名字。
#读取内容：
    if cv2.waitKey(10) == ord('q'):  #设定按q退出
        break

#停止调用，关闭窗口
cap.release()
cv2.destoryAllWindows()  

'''
转载一下
ret frame  = cap.read()
ret frame 是调用 cap.read()的两个返回值 read就是一直调用一直返回很多帧
所以返回的好像是一个连续的视频，
要保证一直调用，所以要一直返回一个true值使它不断继续调用，
所以ret是一个布尔值，返回true则继续调用，返回false说明调用完毕或出现调用错误。
关于frame就是每一帧的图像，是一个三维矩阵。frame是一个类似于文件夹/包，
不断的读取一帧一帧的照片进去，到后面用到窗口显示时，再对frame进行解包，释放出一帧一帧的图像，
就像视频一样。

waitkey()函数功能： 
cv2.waitKey顾名思义等待键盘输入，单位为毫秒，
即等待指定的毫秒数看是否有键盘输入，若在等待时间内按下任意键则返回按键的ASCII码，
程序继续运行。若没有按下任何键，超时后返回-1。参数为0表示无限等待。
不调用waitKey的话，窗口会一闪而逝，看不到显示的图片
————————————————
版权声明：本文为CSDN博主「Sunbeam_c」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/Programmer_ch/article/details/89057129
'''
