import cv2
cap = cv2.VideoCapture(0)
print("VideoCapture is opened?",cap.isOpened())

while(True):
    
    ret, frame = cap.read()
    #center = (frame.shape[1]//2, frame.shape[0]//2)

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.circle(gray, center=center, radius=100, color=(0,0,255))
    cv2.imshow("frame",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

    