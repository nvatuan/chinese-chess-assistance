import cv2 as cv2
import numpy as np
from matplotlib import pyplot as plt

def fitCircle(IMAGE_NAME, DEBUG=False):
    return_val = None

    ## reading image and convert them to hsv
    image = cv2.imread(IMAGE_NAME)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    ## Constant Threshold
    lower = np.array([81, 0, 0])
    upper = np.array([180, 255, 255])

    ## try varying mask to get better result
    mask = cv2.inRange(hsv, lower, upper)
    #kernel = np.ones((10, 10), np.uint8)
    #mask_eroded = cv2.erode(mask, kernel)
    #cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    edge = cv2.Canny(image, 50, 100)
    kernel = np.ones((4, 4), np.uint8)
    edge = cv2.morphologyEx(edge, cv2.MORPH_CLOSE, kernel, iterations=1)

    #kernel = np.ones((2, 2), np.uint8)
    #edge = cv2.dilate(edge, kernel)

    p1 = 1
    p2 = 60
    
    circles = cv2.HoughCircles(edge, cv2.HOUGH_GRADIENT, 1, 20,
        param1=p1, param2=p2, minRadius=20, maxRadius=75 )
    if not (circles is None):
        if len(circles[0]) > 1: return_val = None
        else: return_val = circles[0][0]

        circles = np.uint16(np.around(circles))

    ## Plotting via plt if DEBUG is on
    if DEBUG:
        cimg = image.copy()
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
        
            cv2.imshow('circle', cimg)
    
        ## Plotting
        import matplotlib.pyplot as plt

        plt_img = [image, mask, edge, cimg]
        plt_subtitle = ['Image', 'Mask', 'Edge', 'Circle']

        ### making sure there are enough subtitles
        plt_count = len(plt_img)
        if len(plt_subtitle) < plt_count:
            plt_subtitle.append([''] * (plt_count - len(plt_subtitle)))

        ### pyplot params
        h, w = 100, 100
        s = int(np.sqrt(plt_count))
        axes=[]
        fig=plt.figure()

        for a in range(plt_count):
            b = cv2.resize(plt_img[a], (h, w), interpolation=cv2.INTER_LINEAR)
            axes.append( fig.add_subplot(s, s, a+1) )
            axes[-1].set_title(plt_subtitle[a])  
            plt.axis('off')
            plt.imshow(cv2.cvtColor(b, cv2.COLOR_BGR2RGB))

        fig.tight_layout()    
        plt.waitforbuttonpress(0)
    
    return return_val

def testFitCircle(DIRS, PATH_TO_DIRS = ".", DEBUG = False):
    from os import listdir
    from os.path import isfile, join

    for d in DIRS:
        print("Test fitting on", d)
        
        path = PATH_TO_DIRS + '/' + d + '/'
        onlyfiles = [f for f in listdir(path) if isfile(path + f)]

        found = 0
        total = 0
        fail = []

        for f in onlyfiles:
            if f[-4:] == '.png':
                total += 1
                fwp = path + f
                #print('Testing [', fwp, ']')
                if not (fitCircle(fwp, DEBUG) is None): found += 1
                else: fail.append(fwp)

        print("Detected ", found, "/", total)
        print(fail)
        if len(fail) < 5:
            for f in fail: fitCircle(f, False)

def getIsolatePieceFile(file, RATIO = 1.0):
    piece = cv2.imread(file)

    assert piece.shape[0] == piece.shape[1], "Input piece image should be a square"
    cir = fitCircle(file)

    SIZE = int(piece.shape[0] * RATIO)

    isolated = np.zeros((SIZE, SIZE, 3), np.uint8)
    isolated[:] = (255, 255, 255)      # (B, G, R)

    oy, ox, r = int(round(cir[0])), int(round(cir[1])), cir[2]
    cy, cx = (SIZE - 1)//2, (SIZE - 1)//2 

    dy, dx = (cy - oy), (cx - ox)

    for x in range(SIZE):
        for y in range (SIZE):
            if (x - ox)**2 + (y - oy)**2 <= r**2:
                isolated[x + dx][y + dy] = piece[x][y]
    return isolated

def outputIsolatedPieces(DIRS, PATH_TO_DIRS = ".", OUTPUT_PREFIX = "/iso_"):
    '''
        All dirs relative path should start with only 1 '/'
    '''
    from os import listdir
    from os import mkdir
    from os.path import isfile, join, exists

    assert exists(PATH_TO_DIRS), "Path to DIRS[] (" + PATH_TO_DIRS + ") doesn't exist."

    print("Isolating sets of image:", DIRS)
    for d in DIRS:
        print("Isolating set", d)
        
        input_path = PATH_TO_DIRS + d + '/'
        assert exists(input_path), "Input path (" + input_path + ") doesn't exist."
        onlyfiles = [f for f in listdir(input_path) if isfile(input_path + f)]

        nd = d[1:]
        output_path = PATH_TO_DIRS + OUTPUT_PREFIX + nd + '/'
        if not exists(output_path): mkdir(output_path)

        for f in onlyfiles:
            input_filename = input_path + f
            iso = getIsolatePieceFile(input_filename)
            output_filename = output_path + f
            cv2.imwrite(output_filename, iso)
        
        print("Finished isolating set", d)


if __name__ == "__main__":    
    PATH_TO_DIRS = "./pieces"
    DIRS = ["/set1"]#, "/set2", "/set3", "/set4", "/set5", "/set6", "/set7", "/set12"]

    # testFitCircle(DIRS, PATH_TO_DIRS, False)
    outputIsolatedPieces(DIRS, "./pieces")
