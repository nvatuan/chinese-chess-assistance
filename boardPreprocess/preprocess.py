import numpy as np
import matplotlib.pyplot as plt 
import cv2 

### Constants
IMAGE_NAME = "board2.png"

LOW_HUE, LOW_SAT, LOW_VAL = 91, 0, 0
UPPER_HUE, UPPER_SAT, UPPER_VAL = 180, 255, 255
LOW_HSV = [LOW_HUE, LOW_SAT, LOW_VAL]
UPPER_HSV = [UPPER_HUE, UPPER_SAT, UPPER_VAL]

from os.path import exists
from os import mkdir
OUTPUT_PATH = "./output/"
if not exists(OUTPUT_PATH): mkdir(OUTPUT_PATH)

OUTPUT_HEIGHT, OUTPUT_WIDTH = 3*500, 3*450

### program starts
image = cv2.imread(IMAGE_NAME)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_yellow = np.array(LOW_HSV)
upper_yellow = np.array(UPPER_HSV)

# find mask with LOW_HSV and UPPER_HSV thresholds
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

# erode mask to reduce noise
kernel = np.ones((5, 5), np.uint8)
mask = cv2.erode(mask, kernel)
mask = cv2.bitwise_not(mask)


# find contours with current `mask`
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# approx. all contours into a quadrilateral
approxContours = []
for contour in contours:
    epsilon = 0.1*cv2.arcLength(contour, True)
    approxContours.append(cv2.approxPolyDP(contour,epsilon,True))

# find contour with the max perimeter
def getMaxPerimiterContour(contours, closedContour = True):
    currMaxPeri = 0
    currMaxPeriCont = []
    for currCont in contours:
        currPeri = cv2.arcLength(currCont, closedContour)
        if currPeri > currMaxPeri:
            currMaxPeri, currMaxPeriCont = currPeri, currCont.copy()
    return currMaxPeriCont

boardContour = getMaxPerimiterContour(approxContours)

# get the 4 corner coordinates
## border of board
boardBorder = np.float32([p[0] for p in boardContour])
## border of image
imageBorder = np.float32([[OUTPUT_WIDTH, OUTPUT_HEIGHT], [OUTPUT_WIDTH, 0], [0, 0], [0, OUTPUT_HEIGHT]])

## Test if we got the coords correctly
print(boardBorder)
print(imageBorder)
hl_image = image.copy()
for p in boardBorder:
   cv2.circle(hl_image, tuple(list(map(int, p[:]))), 5, (0, 0, 255), 2) # tuple(list(map(.. because implicit int conversion is deprecated
for p in imageBorder:
   cv2.circle(hl_image, tuple(list(map(int, p[:]))), 5, (0, 255, 255), 2)
cv2.imshow("corners hightlight", hl_image)

# do warping transform so we have top-down view of the board
M = cv2.getPerspectiveTransform(boardBorder, imageBorder)
warped = cv2.warpPerspective(image, M, (OUTPUT_WIDTH, OUTPUT_HEIGHT))

##crop the images to 90 small pieces
cv2.imshow("warped", warped)
cv2.waitKey(0)

cv2.imwrite(OUTPUT_PATH + "/warped.png", warped) # ./output folder should exists before the execution of this line

assert(OUTPUT_HEIGHT//10*9 == OUTPUT_WIDTH) # output height and width should follow ratio 10:9
margin = OUTPUT_HEIGHT//10 # each piece belongs in a square of (OUTPUT_HEIGHT/10) x (OUTPUT_WIDTH/9)

for th in range(0, OUTPUT_HEIGHT, margin):
    for tw in range(0, OUTPUT_WIDTH, margin):
        piece = warped[th:th+margin, tw:tw+margin].copy()
        # cv2.imshow("piece", piece)
        # cv2.waitKey(0)
        name = str(th//margin) + "_" + str(tw//margin) + ".png"
        cv2.imwrite(OUTPUT_PATH + name, piece)


        
