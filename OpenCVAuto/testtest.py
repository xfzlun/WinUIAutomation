import cv2
cap = cv2.VideoCapture(0)  # 创建一个capture实例，这个会返回2个数值，一个布尔值跟一个二进制数组
#ret, frame = cap.read()
#print(ret)
while True:
    ret,frame = cap.read()  #先用read方法读取cap实例
    cv2.imshow("Video", frame)
#显示图像cv2.imshow()
#使用函数cv2.imshow() 显示图像。窗口会自动调整为图像大小。第一个参数是窗口的名字，其次才是我们的图像。你可以创建多个窗口，只要你喜欢，但是必须给他们不同的名字。
#读取内容：
    if cv2.waitKey(0) == ord('q'):  #设定按q退出
        break

#停止调用，关闭窗口
cap.release()
cv2.destroyAllWindows()