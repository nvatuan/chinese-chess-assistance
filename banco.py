import cv2
import numpy as np

chess = cv2.imread(r".\CANVAS.png", 1)
print (chess.shape)
print (chess.dtype)

# px = chess[0][0]
# print (px)
s = cv2.imread(r".\BA.png", 1)
print (s.shape)
print (s.dtype)
# cv2.imshow('BA', s)
# cv2.waitKey(0)
t = cv2.imread(r".\BB.png", 1)
print (t.shape)
# p = cv2.imread(r".\BC.png", 1)
# g = cv2.imread(r".\BK.png", 1)
# m = cv2.imread(r".\BN.png", 1)
# c = cv2.imread(r".\BP.png", 1)
# x = cv2.imread(r".\BR.png", 1)
# S = cv2.imread(r".\RA.png", 1)
# T = cv2.imread(r".\RB.png", 1)
# P = cv2.imread(r".\RC.png", 1)
# G = cv2.imread(r".\RK.png", 1)
# M = cv2.imread(r".\RN.png", 1)
# C = cv2.imread(r".\RP.png", 1)
# X = cv2.imread(r".\RR.png", 1)



# temp = chess
# #temp = cv2.add(chess, s)
#
# # temp = cv2.add(temp,t)
# # temp = cv2.add(temp,p)
# # temp = cv2.add(temp,g)
# # temp = cv2.add(temp,m)
# # temp = cv2.add(temp,c)
# # temp = cv2.add(temp,x)
# # temp = cv2.add(temp,S)
# # temp = cv2.add(temp,T)
# # temp = cv2.add(temp,C)
# # temp = cv2.add(temp,G)
# # temp = cv2.add(temp,M)
# # temp = cv2.add(temp,C)
# # temp = cv2.add(temp,X)
#
cv2.imshow('ban co', chess)
cv2.waitKey(0)
# cv2.destroyAllWindows()
