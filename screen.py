import numpy as np
from PIL import ImageGrab
from collections import deque
import cv2
import time
import imutils
import argparse
import cv2 as CV
import socket
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


TCP_IP = '192.168.2.2' 
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print ("received data:", data)

x = 0 #programın ileride hata vermemesi için x 0 olarak tanımlıyorum
y = 0 # programın ileride hata vermemesi için y 0 olarak tanımlıyorum


colorLower = (80,100,100)
colorUpper = (100,255,255)


def renk1():
    colorLower = (80,100,100)
    colorUpper = (100,255,255)
def renk2():
    colorLower = (80,100,100)
    colorUpper = (100,255,255)


def screen_record():
    hedef = 0
    tarama = 0
    x = 0
    y = 0
    r = 0
    last_time = time.time()
    while(True):
        # 800x600 windowed mode
        printscreen =  np.array(ImageGrab.grab(bbox=(110,200,1710,760)))
        print('Tekrarlanma süresi : {} saniye'.format(time.time()-last_time))
        last_time = time.time()

        frame = printscreen
        frame = imutils.resize(frame, width=600 , height= 600)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        else:
            x = 0
            y = 0
            r = 0

        print("x : ")
        print(x)
        print("y : ")
        print(y)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        if(hedef == 0):

            if(x > 750 and x < 900 ):
                MESSAGE = "ileri"
                if(r > 100):
                    time.sleep(3)
                    cv2.imwrite('harf.png', frame)
                    im = Image.open("harf.png")
                    text = pytesseract.image_to_string(im, lang = 'eng')
                    print(text)
                    time.sleep(5)

            elif(x < 750):
                MESSAGE = "sol"
            elif(x > 900):
                MESSAGE = "sag"
        elif(hedef == 1):
            if(100 > tarama):
                tarama +=1
                MESSAGE = "ileri"
            elif(99 < tarama < 110 ):
                tarama +=1
                MESSAGE = "don"
            else:
                tarama =0


screen_record()
