import time
import cv2
import numpy as np
print(cv2.__version__)
fps = 10
frame_width = 640
frame_height = 360
flip = 0
camSet='v4l2src device=/dev/video2 ! video/x-raw! videoconvert ! appsink'
cam=cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
cam.set(cv2.CAP_PROP_FPS, fps)
motion_threshold = 2400
print(cam)
time.sleep(1)

if cam.isOpened() is not True:
    print("Cannot open camera. Exiting.")
    cam.release()
    quit()
n=0 # изменяем размеры экрана чтобы отображать его на 5-дюймовом TFT дисплее
kernal = np.ones((5,5),np.uint8)
lastMotion = time.time()
while True:
    _, frame1 = cam.read() # считываем первый кадр
    grayImage_F1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)  # конвертируем его в серое изображение
    _, frame2 = cam.read() # считываем второй кадр
    grayImage_F2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diffImage = cv2.absdiff(grayImage_F1,grayImage_F2) #определяем разницу между двумя кадрами 
    blurImage = cv2.GaussianBlur(diffImage, (5,5), 0)
    _, thresholdImage = cv2.threshold(blurImage, 20,255,cv2.THRESH_BINARY)
    dilatedImage = cv2.dilate(thresholdImage,kernal,iterations=5)
    f, contours, o = cv2.findContours (dilatedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) #find contour is a magic function
    for contour in contours: #for every change that is detected
        (x,y,w,h) = cv2.boundingRect(contour) # находим местоположение где зафиксировано изменение
        if cv2.contourArea(contour) > motion_threshold:
            if (time.time() - lastMotion > 1):
                print("I see x "+str(n))
                n+=1
                lastMotion = time.time()
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 1)
            display_screen = frame2

    
    dim = (1280, 720)
    Full_frame = cv2.resize (frame2,dim,interpolation=cv2.INTER_AREA)
    cv2.namedWindow("AISHA", cv2.WINDOW_NORMAL)
    cv2.imshow("AISHA",Full_frame)
    if cv2.waitKey(1)==ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        break


