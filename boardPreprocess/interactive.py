import numpy as np
import matplotlib.pyplot as plt 
import cv2 

### =================== DETECTING COLOR (or Thresholding the image)
IMAGE_NAME = "testStand_small.png"

def nothing(x):
    pass

### activate trackbars
cv2.namedWindow('Trackbar')
cv2.createTrackbar("L-H", "Trackbar", 91, 180, nothing)
cv2.createTrackbar("L-S", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("L-V", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("U-H", "Trackbar", 180, 180, nothing)
cv2.createTrackbar("U-S", "Trackbar", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbar", 255, 255, nothing)

while True:
    image = cv2.imread(IMAGE_NAME)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "Trackbar")
    l_s = cv2.getTrackbarPos("L-S", "Trackbar")
    l_v = cv2.getTrackbarPos("L-V", "Trackbar")
    u_h = cv2.getTrackbarPos("U-H", "Trackbar")
    u_s = cv2.getTrackbarPos("U-S", "Trackbar")
    u_v = cv2.getTrackbarPos("U-V", "Trackbar")

    lower_yellow = np.array([l_h, l_s, l_v])
    upper_yellow = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    mask = cv2.bitwise_not(mask)

    cv2.imshow('mask', mask)
    cv2.imshow('image', image)

    ## Hit 'q' to finish adjusting the threshold
    key = cv2.waitKey(1)
    if key == ord('q'):
        cv2.destroyAllWindows()
        break

### =================== CONTOUR FINDING

#dilated = cv2.dilate(mask, kernel, iterations=3)
#cv2.imshow('mask dilated', dilated)

contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#tmp = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(image, contours, 0, (0, 255, 0), 3)


# contours is a list of contour detected in the image
for i, cnt in enumerate(contours):
    print("Contour #%d/%d" % (i, len(contours)))
    tmpImage = image.copy()

    cv2.drawContours(tmpImage, [cnt], 0, (0, 255, 0), 3)

    ### Approx contour to a polygon shape
    ### Works: the board has rough edges and some protrude parts, approx. trims those.
    epsilon = 0.1*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)
    ## highlight the approx contour (4 sides)
    cv2.drawContours(tmpImage, [approx], 0, (0, 0, 255), 2)
    print("Approx. contour sides:", len(approx))

    ### Fit bounding rectangle
    ### Doesn't work: It tries to fit every thing to a rectangle, ie. doesn't trim.
    #rect = cv2.minAreaRect(cnt)
    #box = cv2.boxPoints(rect)
    #box = np.int0(box)
    #cv2.drawContours(tmpImage,[box], 0, (0, 0, 255), 2)

    ### highlights the approx contour corners as blue dots
    for ap in approx:
        cv2.circle(tmpImage, (ap[0][0], ap[0][1]), 7, (255, 0, 0), -1)

    cv2.imshow("contour highlight", tmpImage)
    while True:
        key = cv2.waitKey(1)
        ## Press n to go to the next Contour
        if key == ord('n'): break
        ## Press q to quit
        if key == ord('q'): exit(0)