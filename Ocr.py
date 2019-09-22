from PIL import Image
import pytesseract
import time
import numpy as np
from PIL import ImageGrab
from collections import deque
import cv2
import imutils
import argparse
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import ImageGrab
 

tx = 0
while(True):
	printscreen =  np.array(ImageGrab.grab(bbox=(50,50,1710,900)))
	frame = printscreen
	cv2.imwrite('1.jpg', frame)
	time.sleep(1)
	print("goruntu aliniyor")
	im = Image.open("1.jpg")
	text = pytesseract.image_to_string(im, lang = 'eng')
	text.strip("	")
	text.strpi(" ")
	try:
		print(text)
		cv2.imwrite(text + ".jpg", frame)
		file = open(text + ".txt","w")
		file.write(str(text))
	except(FileNotFoundError):
		print("Algilanmadi")
