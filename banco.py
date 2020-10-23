import cv2
import numpy as np

chess = cv2.imread(r".\CANVAS.png", 1)
s = cv2.imread(r".\BA.png", 2)
# t = cv2.imread(r"C:\Users\ASUS\PycharmProjects\DoAnKy5\Anhco\BB.gif", 3)
# p = cv2.imread(r"C:\Users\ASUS\PycharmProjects\DoAnKy5\Anhco\BC.gif", 4)
# g = cv2.imread(r"C:\Users\ASUS\PycharmProjects\DoAnKy5\Anhco\BK.gif", 5)
# m = cv2.imread(r"C:\Users\ASUS\PycharmProjects\DoAnKy5\Anhco\BN.gif", 6)
# c = cv2.imread(r"C:\Users\ASUS\PycharmProjects\DoAnKy5\Anhco\BP.gif", 7)
# x = cv2.imread(r"C:\Users\ASUS\PycharmProjects\DoAnKy5\Anhco\BR.gif", 8)
# S = cv2.imread(r"C:\Users\ASUS\PycharmProjects\DoAnKy5\Anhco\RA.gif", 12)
# T = cv2.imread(r"C:\Users\ASUS\PycharmProjects\DoAnKy5\Anhco\RB.gif", 13)
# P = cv2.imread(r"C:\Users\ASUS\PycharmProjects\DoAnKy5\Anhco\RC.gif", 14)
# G = cv2.imread(r"C:\Users\ASUS\PycharmProjects\DoAnKy5\Anhco\RK.gif", 15)
# M = cv2.imread(r"C:\Users\ASUS\PycharmProjects\DoAnKy5\Anhco\RN.gif", 16)
# C = cv2.imread(r"C:\Users\ASUS\PycharmProjects\DoAnKy5\Anhco\RP.gif", 17)
# X = cv2.imread(r"C:\Users\ASUS\PycharmProjects\DoAnKy5\Anhco\RR.gif", 18)



# temp = chess
temp = cv2.add(chess, s)

# temp = cv2.add(temp,t)
# temp = cv2.add(temp,p)
# temp = cv2.add(temp,g)
# temp = cv2.add(temp,m)
# temp = cv2.add(temp,c)
# temp = cv2.add(temp,x)
# temp = cv2.add(temp,S)
# temp = cv2.add(temp,T)
# temp = cv2.add(temp,C)
# temp = cv2.add(temp,G)
# temp = cv2.add(temp,M)
# temp = cv2.add(temp,C)
# temp = cv2.add(temp,X)

cv2.imshow('ban co', temp)
cv2.waitKey(0)
cv2.destroyAllWindows()
