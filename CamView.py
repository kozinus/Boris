import time
import cv2

fps = 15
frame_width = 640
frame_height = 360
flip = 0
camSet='v4l2src device=/dev/video0 ! videoconvert ! video/x-raw, format=BGR ! queue ! appsink'
cam=cv2.VideoCapture(0)

time.sleep(1)

if cam.isOpened() is not True:
    print("Cannot open camera. Exiting.")
    cam.release()
    quit()
    
while True:
    ret, frame = cam.read()

    cv2.imshow('webcam',frame)
    cv2.moveWindow('webcam',0,0)
    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
