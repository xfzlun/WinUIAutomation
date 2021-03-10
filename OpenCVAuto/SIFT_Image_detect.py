import cv2
import matplotlib.pyplot as plt
# load image
img = cv2.imread('rameses.jpg')
# convert to grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# instantiate SURF
surf = cv2.xfeatures2d.SURF_create(7000)
# compute keypoints
kp = surf.detect(img_gray, None)
# plot keypoints
plt.imshow(cv2.drawKeypoints(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), kp, None, (0,255,0), 4))
plt.show()