import cv2
import numpy as np

img1 = cv2.imread("CANVAS.png",1)
img2 = cv2.imread("BA.png",1)

img1 = img1[513:570 , 456:513]
img2 = img2[0:57 , 57:114]

#img2 = img2[0:57 , 0:57] # Quân Cờ
#img3 = cv2.add(img1, img2)
cv2.imshow('image', img1)
cv2.waitKey(0)