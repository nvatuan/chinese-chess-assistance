# loggings
import traceback
import time

# multithread
import threading

# image processing
import numpy as np
import cv2

# camera
from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
time.sleep(0.1)

class VideoProcessor(threading.Thread):
    camera = None
    camera_resolution, camera_framerate = None, None
    modulePreprocess, moduleXiangpiRender, moduleGuesser = None, None, None
    rawFrame = maskFrame = contourFrame = topDownView = canvasFrame = np.zeros((5, 5, 3), dtype=np.uint8)
    descriptorString = None

    __maxContourSize = None
    __setCanvasFrameThreadLock = threading.Lock()
    __setCanvasFrameThreadSpawned = False
    

    classLock = None
    AllowedGet = False
    INS_JOBS = ['processor', 'get-raw', 'get-mask', 'get-contour', 'get-canvas']
    #RET_VAL = {'get-raw' : None, 'get-mask' : None, 'get-contour' : None, 'get-canvas' : None}

    def __init__(self, job, modulePreprocess=None, moduleXiangpiRender=None, moduleGuesser=None, resolution=None, framerate=None):
        super(VideoProcessor, self).__init__()
        assert job in VideoProcessor.INS_JOBS, 'Instance job is unknown'
        self.job = job
        if self.job == 'processor':
            assert not framerate is None, 'As a processor, passed arguments must not be empty'
            assert VideoProcessor.camera is None, 'Only one instance classified as a \'processor\' is allowed.'
            initClassvar(modulePreprocess, moduleXiangpiRender, moduleGuesser, resolution, framerate)
        else:
            assert not VideoProcessor.camera is None, 'There is no camera yet!'
    
    def run(self):
        if self.job == 'processor':
            self.startVideoCapture()
        else:
            # while VideoProcessor.AllowedGet != True: pass
            # self.handler = {
            #     'get-raw' : VideoProcessor.getRawFrame, 'get-mask' : VideoProcessor.getMaskFrame,
            #     'get-contour' : VideoProcessor.getContourFrame, 'get-canvas' : VideoProcessor.getCanvasFrame
            # }
            # classLock.acquire(1)
            # VideoProcessor.RET_VAL[self.job] = VvideoProcessor.andler[self.job]()
            # classLock.release()
            return
            
    ## getters -------------------------------------------------
    def getRawFrame(self):
        return VideoProcessor.rawFrame
        
    def getMaskFrame(self):
        return VideoProcessor.maskFrame

    def getContourFrame(self):
        return VideoProcessor.contourFrame

    def getTopDownView(self):
        return VideoProcessor.topDownView

    def getCanvasFrame(self):
        return VideoProcessor.canvasFrame

    ## setters -------------------------------------------------
    def setRawFrame(self, frame):
        VideoProcessor.classLock.acquire(1)
        VideoProcessor.rawFrame = frame
        VideoProcessor.classLock.release()

    def setMaskFrame(self, frame):
        tmpMask = VideoProcessor.preprocess.maskedByThresholding(frame)
        VideoProcessor.classLock.acquire(1)
        VideoProcessor.maskFrame = tmpMask
        VideoProcessor.classLock.release()
    
    def setContourFrame(self, frame):
        VideoProcessor.classLock.acquire(1)
        mask = self.getMaskFrame().copy()
        VideoProcessor.classLock.release()

        raw = frame.copy()
        tmpCnt = frame.copy()
    
        ## contours
        bcnts = VideoProcessor.preprocess.getMaxPerimeterContourOfMask(mask)
        
        cv2.drawContours(tmpCnt, [bcnts], 0, (0,0,255), 2)
        bcnts = VideoProcessor.preprocess.approxContour(bcnts)
        cv2.drawContours(tmpCnt, [bcnts], 0, (0,255,0), 2)
        VideoProcessor.preprocess.putCircle(tmpCnt, bcnts)

        ## topdown
        tmpTopDownView = VideoProcessor.preprocess.getTopDownOfImage(
            raw, bcnts, False, 500, 450
        )

        ## set variables
        VideoProcessor.classLock.acquire(1)
        VideoProcessor.contourFrame, VideoProcessor.topDownView = tmpCnt, tmpTopDownView       
        VideoProcessor.classLock.release()
    
    def setCanvasFrame(self):
        VideoProcessor.classLock.acquire(1)
        topdown = self.getTopDownView().copy()
        VideoProcessor.classLock.release()

        try:
            pieces = VideoProcessor.preprocess.splice10by9(topdown)
            desc = ''
            #print('Start predicting 90 samples..'); t = time.time()
            for piece in pieces:
                g = VideoProcessor.Guesser.guess(piece, True)
                desc += g
            bking = g.find('g')
            rking = g.find('G')
            if not (0 <= rking <= 44 and 45 <= bking <= 89):
                desc = desc[::-1]
                    
            #print('Finished predicting: %f(s)' % (time.time() - t))
            canvas = VideoProcessor.XiangpiRender.renderBoard(desc, False, '', '/texture')
            #canvas = cv2.resize(canvas, (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

            VideoProcessor.classLock.acquire(1)
            VideoProcessor.canvasFrame = canvas
            VideoProcessor.descriptorString = desc
            VideoProcessor.classLock.release()
        except Exception as e:
            print('Cannot detect the board.')
            time.sleep(1)
        finally:
            # release the thread
            print('>> Finished canvas job %f(s).' % (
                time.time() - VideoProcessor.__setCanvasFrameThreadSpawnedTimestamp)
            )
            #VideoProcessor.__setCanvasFrameThreadSpawned = False
            VideoProcessor.__setCanvasFrameThreadLock.release()
    
    ## -----------------------------------------------------------        

    def startVideoCapture(self):    
        with picamera.array.PiRGBArray(VideoProcessor.camera, VideoProcessor.camera_resolution) as output:
            VideoProcessor.camera.start_preview()
            VideoProcessor.AllowedGet = True # start accept getting request
            while True:
                try:
                    VideoProcessor.camera.capture(output, 'rgb')
                    frame = output.array.copy() # copy to object in memory
                    output.truncate(); output.seek(0) # reset buffer

                    t = time.time()
                    #print('! Send raw started.')
                    self.setRawFrame(frame)
                    #print(time.time() - t); t = time.time()
                    self.setMaskFrame(frame)
                    #print('! Send mask started.')
                    #print(time.time() - t); t = time.time()
                    #print('! Send contour started.')
                    self.setContourFrame(frame)
                    #print(time.time() - t); t = time.time()
                    #print('! Done started.')

                    ## start a separate thread for Canvas (heavy task)
                    #if VideoProcessor.__setCanvasFrameThreadSpawned == False:
                    if VideoProcessor.__setCanvasFrameThreadLock.acquire(0):
                        print('>> No thread is currently processing canvas, spawning..')
                        # lock the thread so no multiple thread doing the same task
                        VideoProcessor.__setCanvasFrameThreadSpawnedTimestamp = time.time()
                        #VideoProcessor.__setCanvasFrameThreadSpawned = True

                        th = threading.Thread(target=self.setCanvasFrame)
                        th.start()
                    else:
                        #print('>> There is a thread currently processing canvas. Ignoring job.')
                        pass
                    ## single threaded
                    #self.setCanvasFrame()
                    #print('! Routine finished %f(s)\n' % (time.time() - t))

                    time.sleep(0.1)                    
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    VideoProcessor.camera.stop_preview()
                    break
                finally:
                    pass
                    

def initClassvar(modulePreprocess=None, moduleXiangpiRender=None, moduleGuesser=None, resolution=None, framerate=None):
    VideoProcessor.camera = PiCamera()
    VideoProcessor.camera.resolution = VideoProcessor.camera_resolution = resolution
    VideoProcessor.camera.framerate = VideoProcessor.camera_framerate = framerate

    VideoProcessor.preprocess = modulePreprocess
    VideoProcessor.XiangpiRender = moduleXiangpiRender
    VideoProcessor.Guesser = moduleGuesser
    
    VideoProcessor.__setCanvasFrameThreadLock = threading.Lock()
    VideoProcessor.classLock = threading.Lock()
    
def threadsafe_getRawFrame(mut):
    VideoProcessor.classLock.acquire(1)
    mut.append(VideoProcessor.rawFrame)
    VideoProcessor.classLock.release()
    
def threadsafe_getMaskFrame(mut):
    VideoProcessor.classLock.acquire(1)
    mut.append(VideoProcessor.maskFrame)
    VideoProcessor.classLock.release()

def threadsafe_getContourFrame(mut):
    VideoProcessor.classLock.acquire(1)
    mut.append(VideoProcessor.contourFrame)
    VideoProcessor.classLock.release()

def threadsafe_getTopDownView(mut):
    VideoProcessor.classLock.acquire(1)
    mut.append(VideoProcessor.topDownView)
    VideoProcessor.classLock.release()

def threadsafe_getCanvasFrame(mut):
    VideoProcessor.classLock.acquire(1)
    mut.append(VideoProcessor.canvasFrame)
    VideoProcessor.classLock.release()
    
def threadsafe_getDescriptorString(mut):
    VideoProcessor.classLock.acquire(1)
    mut.append(VideoProcessor.descriptorString)
    VideoProcessor.classLock.release()