import cv2 as cv
import os

cap = cv.VideoCapture(1)
ret, frame = cap.read()
print(os.getcwd())

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
select_place(frame)