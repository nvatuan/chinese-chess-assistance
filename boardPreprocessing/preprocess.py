import numpy as np
import matplotlib.pyplot as plt 
import cv2 

def maskedByHoughLines(img):
    ## constant
    CANNY_T1, CANNY_T2 = 130, 0

    ##
    img = cv2.blur(img, (11, 11))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(gray, CANNY_T1, CANNY_T2)

    kernel = np.ones((3, 3))
    morph = cv2.dilate(imgCanny, kernel, iterations=1)
    #kernel = np.ones((2, 2))
    #morph = cv2.erode(morph, kernel, iterations=1)
    #kernel = np.ones((10, 10))
    #morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow('can', morph)

    lines = cv2.HoughLinesP(morph, 1, np.pi/180, 130, maxLineGap=100)
    mask = np.zeros(shape=imgCanny.shape, dtype=np.uint8)
    
    try:
        for l in lines:
            x1, y1, x2, y2 = l[0]
            cv2.line(blank, (x1, y1), (x2, y2), (255, 255, 255), 2)
    except:
        pass
    return mask 

def maskedByThresholding(image):
    LOW_HUE, LOW_SAT, LOW_VAL = 91, 0, 0
    UPPER_HUE, UPPER_SAT, UPPER_VAL = 180, 255, 255
    LOW_HSV = [LOW_HUE, LOW_SAT, LOW_VAL]
    UPPER_HSV = [UPPER_HUE, UPPER_SAT, UPPER_VAL]

    image = cv2.blur(image, (3, 3))
    #image = cv2.bilateralFilter(image, 5, 100, 10)
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    
    lower_yellow = np.array(LOW_HSV)
    upper_yellow = np.array(UPPER_HSV)

    # find mask with LOW_HSV and UPPER_HSV thresholds
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    mask = cv2.bitwise_not(mask)
    
    # erode mask to reduce noise
    kernel = np.ones((40, 40), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    #mask = cv2.erode(mask, kernel)
    

    return mask

def approxContour(contour):
    epsilon = 0.05*cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour,epsilon,True)
    return approx
    
# find contour with the max perimeter
def getMaxPerimeterContourOfMask(mask, closedContour = True):
    # find contours with current `mask`
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    currMaxPeri = 0
    currMaxPeriCont = []
    for currCont in contours:
        currPeri = cv2.arcLength(currCont, closedContour)
        if currPeri > currMaxPeri:
            currMaxPeri, currMaxPeriCont = currPeri, currCont.copy()
    return currMaxPeriCont

# get the 4 corner coordinates
## border of board

def getTopDownOfImage(image, boardContour, debug=False, OUTPUT_HEIGHT=500, OUTPUT_WIDTH=450):
    ''' Given a image and the board's contour, this function returns an image of 
    only the board and as if it were being view from a straight top-down angle using
    Perspective Warping.
        The boardContour is expected to have its length == 4, because the board is a rectangle.
        This function always return a tuple. If debug is False, the tuple is (warped,)
        If debug is True, the tuple is (warped, image_but_has_detected_corners_highlighted)
    '''
    def topLeftCCW(pts):
        '''pts is a list of 2-element list and they are X and Y coords of a polygon, given in ccw order.
        This function finds the matching orientation to the pre-defined orientation of
        [topLeft, bottomLeft, bottomRight, topRight] based on the longest side of the contour.
        '''
        def EuclidDistSqr(i, nxt_i):
            return (pts[i][0] - pts[nxt_i][0])**2 + (pts[i][1] - pts[nxt_i][1])**2
        ## ----

        longestIdx, longest = 0, -1
        n = len(pts)
        for i in range(0, n):
            nxt_i = (i + 1) % n
            if EuclidDistSqr(i, nxt_i) > longest:
                longest, longestIdx = EuclidDistSqr(i, nxt_i), i
    
        orient = []
        curr = longestIdx
        for i in range(0, n):
            orient.append(pts[curr])
            curr = (curr + 1) % n
        return orient
    ## -----

    boardBorder = np.float32(topLeftCCW([p[0] for p in boardContour]))
    topdownBorder = np.float32([[0, 0], [0, OUTPUT_HEIGHT], [OUTPUT_WIDTH, OUTPUT_HEIGHT], [OUTPUT_WIDTH, 0]])
    
    # do warping transform so we have top-down view of the image
    try:
        M = cv2.getPerspectiveTransform(boardBorder, topdownBorder)
        warped = cv2.warpPerspective(image, M, (OUTPUT_WIDTH, OUTPUT_HEIGHT))
    except:
        if not debug: return image
        return image, boardBorder

    if not debug: return warped
    
    return warped, boardBorder

def putCircle(image, pts):
    ''' This function put circles at points in pts '''
    try:
        for p in pts:
            cv2.circle(image, tuple(list(map(int, p[0][:]))), 5, (255, 0, 0), 2) # tuple(list(map(.. because implicit int conversion is deprecated
        return True
    except:
        return False


def splice10by9(image, writeToDisk=False, OUTPUT_PATH = "./output/"):
    ''' This function cuts the image into 90 smaller, equal size square pieces.
        Because of that, image's size has to abide the 10:9 ratio.

        Then return a 2d list, each containing pieces on the same row with left-to-right order

        if writeToDisk is True, the function attempts to write 90 images to OUTPUT_PATH
    '''
    height, width, channels = image.shape

    assert(height//10 == width//9) # output height and width should follow ratio 10:9
    margin = height//10 # each piece belongs in a square of (height/10) x (width/9)

    if writeToDisk:
        from os.path import exists
        from os import mkdir
        if not exists(OUTPUT_PATH): mkdir(OUTPUT_PATH)
    
    pieces = []
    for th in range(0, height, margin):
        for tw in range(0, width, margin):
            piece = image[th:th+margin, tw:tw+margin].copy()
            if writeToDisk:
                name = str(th//margin) + "_" + str(tw//margin) + ".png"
                cv2.imwrite(OUTPUT_PATH + name, piece)
            pieces.append(piece)

    return pieces

def fromAtoZ(image, useHoughLines=False):
    try:
        if useHoughLines: mask = maskedByHoughLines(image)
        else: mask = maskedByThresholding(image)
        boardContour = getMaxPerimeterContourOfMask(mask)
        boardContour = approxContour(boardContour)
        pieces = splice10by9(getTopDownOfImage(image, boardContour))
        return pieces
    except:
        return None

if __name__ == "__main__":
    filename = "cam_small.png"

    image = cv2.imread(filename)
    mask = maskedByThresholding(image)
    #mask = maskedByHoughLines(image)

    boardContour = getMaxPerimeterContourOfMask(mask)
    boardContour = approxContour(boardContour)

    board = getTopDownOfImage(image, boardContour, False, 500, 450)
    splice10by9(board)

    cv2.imshow('bord', board)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
