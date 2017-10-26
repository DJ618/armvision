import cv2
import os

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

cv2.imshow('frame', rgb)
if os.path.isfile('currentcapture.jpg'):
    os.remove('currentcapture.jpg')
    
out = cv2.imwrite('currentcapture.jpg', frame)
cap.release()
cv2.destroyAllWindows()
