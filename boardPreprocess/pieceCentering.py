import cv2 as cv2
import numpy as np
from matplotlib import pyplot as plt

def fitCircle(IMAGE_NAME, debug=False):
    return_val = None

    image = cv2.imread(IMAGE_NAME)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array([81, 0, 0])
    upper = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)
    #kernel = np.ones((10, 10), np.uint8)
    #mask_eroded = cv2.erode(mask, kernel)
    #cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    edge = cv2.Canny(image, 50, 100)
    kernel = np.ones((4, 4), np.uint8)
    edge = cv2.morphologyEx(edge, cv2.MORPH_CLOSE, kernel, iterations=1)

    #kernel = np.ones((2, 2), np.uint8)
    #edge = cv2.dilate(edge, kernel)

    if debug:
        cv2.imshow('mask', mask)        
        cv2.imshow('canny', edge)
        cv2.imshow('image', image)

    p1 = 1
    p2 = 60
    
    cimg = image.copy()
    circles = cv2.HoughCircles(edge, cv2.HOUGH_GRADIENT, 1, 20,
                            param1=p1,param2=p2,minRadius=20,maxRadius=75)
    if not (circles is None):
        if len(circles[0]) > 1: return_val = None
        else: return_val = circles[0][0]

        circles = np.uint16(np.around(circles))
        if debug:
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
            
                cv2.imshow('circle', cimg)

    ## Hit 'q' to finish adjusting the threshold
    if debug: cv2.waitKey(0)
    #key = cv2.waitKey(1)
    #if key == ord('q'):
    return return_val

PREFIX = "./pieces"
DIRS = ["/set12"]

def testFitCircle():    
    from os import listdir
    from os.path import isfile, join

    for d in DIRS:
        print("Test fitting on ", d)
        
        path = PREFIX + d + '/'
        onlyfiles = [f for f in listdir(path) if isfile(path + f)]

        found = 0
        total = 0
        fail = []

        for f in onlyfiles:
            if f[-4:] == '.png':
                total += 1
                fwp = path + f
                #print('Testing [', fwp, ']')
                if not (fitCircle(fwp, True) is None): found += 1
                else: fail.append(fwp)

        print("Detected ", found, "/", total)
        print(fail)
        if len(fail) < 5:
            for f in fail: fitCircle(f, False)

def getIsolatePieceSign(file):
    SIZE = 150

    isolated = np.zeros((SIZE, SIZE, 3), np.uint8)
    isolated[:] = (255, 255, 255)      # (B, G, R)

    piece = cv2.imread(file)
    cir = fitCircle(file)

    oy, ox, r = round(cir[0]), round(cir[1]), cir[2]
    cy, cx = (SIZE - 1)//2, (SIZE - 1)//2 

    dy, dx = (cy - oy), (cx - ox)

    for x in range(SIZE):
        for y in range (SIZE):
            if (x - ox)**2 + (y - oy)**2 <= r**2:
                isolated[x + dx][y + dy] = piece[x][y]
    return isolated

from os import listdir
from os import mkdir
from os.path import isfile, join, exists

for d in DIRS:
    path = PREFIX + d + '/'
    onlyfiles = [f for f in listdir(path) if isfile(path + f)]

    output_path = PREFIX + '/iso_' + d[1:] + '/'
    
    if not exists(output_path): mkdir(output_path)

    for f in onlyfiles:
        fwp = path + f
        image = getIsolatePieceSign(fwp)

        small = cv2.resize(image, (0,0), fx=50/150, fy=50/150) 
        cv2.imwrite(output_path + f, small)
        