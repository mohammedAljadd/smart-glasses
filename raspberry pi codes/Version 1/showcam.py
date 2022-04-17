import cv2

cam = cv2.VideoCapture("http://192.168.1.99:8080/video")
while True:
    _, img = cam.read()
    img = cv2.resize(img, (740, 480)) 
    cv2.imshow('my webcam', img)
    if cv2.waitKey(1) == 27: 
        break  # esc to quit


cam.release()
cv2.destroyAllWindows()