#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import argparse
import cv2
import cv2 as CV #eğer python2 kullanıyorsanız eklemek zorundasınız aksi halde hata alırsınız
import time
import threading
from pymavlink import mavutil


cap = cv2.VideoCapture(0) # webcamin bagli oldugu yer
master = mavutil.mavlink_connection( # aracin baglantisi
            '/dev/ttyACM0',
            baud=115200)

#master = "mavutil.mavlink_connection('udpin:192.168.2.2:14550')" #eğer bilgisayardan konttrol edilecekse
def set_rc_channel_pwm(id, pwm=1500):

    if id < 1:
        print("Channel does not exist.")
        return


    if id < 9: # ardusubla iletisim
        rc_channel_values = [65535 for _ in range(8)]
        rc_channel_values[id - 1] = pwm
        master.mav.rc_channels_override_send(
            master.target_system,
            master.target_component,
            *rc_channel_values)


#aracin haraketleri
def ileri():
    set_rc_channel_pwm(5, 1650) # ileri git
def geri():
    set_rc_channel_pwm(5, 1400) # geri git
def sol():
    set_rc_channel_pwm(6, 1400)
def sag():
    set_rc_channel_pwm(6, 1600)
def alcal():
    set_rc_channel_pwm(3, 1400)
def yuksel():
    set_rc_channel_pwm(3, 1600)
def don():
    set_rc_channel_pwm(4, 1400)
l = 0
a = 0 # taramak icin
def bas(): # allahina kadar yardir
  t = threading.Timer(0.0, bas).start()
  set_rc_channel_pwm(3, 1510)
  ileri()
  threading.currentThread()

cap.set(3,1280) #goruntu boyutu
cap.set(3,720)

hedef = 0 #algilandi veya algilanmadi

while(True):
    # goruntu yakalama
    ret, frame = cap.read()
    # goruntuyu grilestir
    output = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # goruntuyu blurlastir
    gray = cv2.GaussianBlur(gray,(5,5),0);
    gray = cv2.medianBlur(gray,5)
    gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,3.5)
    kernel = np.ones((5,5),np.uint8)
    gray = cv2.erode(gray,kernel,iterations = 1)
    gray = cv2.dilate(gray,kernel,iterations = 1)
    #circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 400, param1=40, param2=45, minRadius=0, maxRadius=0) # python$
    circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 300, param1=30, param2=25, minRadius=30, maxRadius=0) #py$
    # kalibre
    # daireyi isle
    if circles is not None:
        # x y kordinatlarini integer cevir
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles: #daireyi işaretle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            print ("X kordinat: ")
            print (x)
            print ("Y Kordinat: ")
            print (y)
            print ("Radius: ")
            print(r)

    else: # hedef algilanmiyorsa degerleri sifirla
        x=0
        y=0
        r=0
    if(x > 1 ):
        hedef = 1

#daireyi ortala ve yardır
    if(hedef == 1):
         if (x == 0 and y == 0): #hedef algilanmadiysa
            if (l < 5):
                 l +=1
                 sol()
                 print("hedef algilanmadi tarama moduna dönüyorum... ")
            else:
                 hedef = 0
         elif (x > 250 and x < 350 ): # hedef ortadaysa
          bas()
          print("duz gidiliyor")
         elif (x < 250): # hedef robotun solunda kalıyorsa
          sol()
          time.sleep(0.2)
          sol()
          time.sleep(0.2)
          sol()
          print("Sol'a dönülüyor...")
         #if (y < 240):
         #    set_rc_channel_pwm(3, 1600 ) # robotun havalanmasi
         #elif (y > 270):
          #   set_rc_channel_pwm(3, 1400) # robotun alcalmasi deger random girildi alcalma pwm bulunduktan sonra degistirilicek
         elif (x > 350): # hedef robotun saginda kaliyorsa
          sag()
          time.sleep(0.2)
          sag()
          time.sleep(0.2)
          sag()
          print("Sag'a dönülüyor...")
    elif(hedef == 0):

         if(150 > a):
           a += 1
           ileri()
           time.sleep(0.2)
           ileri()
           time.sleep(0.2)
           ileri()
           print("havuz taramasi ileri")
           print(a)
         elif(149 < a < 160 ):
            a +=1
           don()
           print("havuz taramasi donuyor")
           print(a)
         else:
           a = 0


cap.release()
cv2.destroyAllWindows()


