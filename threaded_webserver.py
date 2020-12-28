## important libraries
import logging
import traceback

#
import numpy as np
from PIL import Image
import cv2

import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # set tensorflow verbosity up so it won't print much
from threading import Thread

## adding my lib to sys path
import sys
sys.path.insert(1, './boardRendering/')
sys.path.insert(1, './pieceRecognize/')
sys.path.insert(1, './boardPreprocessing/')
sys.path.insert(1, './cchessEngine/')

## my libraries
import preprocess
import XiangpiRender
Guesser = None
from webserverVideoProcessing import VideoProcessor
import webserverVideoProcessing as vpGet

import elephantfish

DF_TFMODEL_DIR = './pieceRecognize/models/G_1milparam_1000epc'
DF_TFLMODEL_DIR = './pieceRecognize/models/G_1milparam_1000epc.tflite'
MODEL_DIR = None
DEBUG_MODE = False
USE_TFLITE = True
RESOLUTION = (640, 480)
DEBUG_RESO = (640, 480)

def preload():
    global DF_TFLMODEL_DIR, DF_TFMODEL_DIR
    global MODEL_DIR, DEBUG_MODE, USE_TFLITE, RESOLUTION
    
    if len(sys.argv) < 2 or sys.argv[1] == 'help':
        print('Syntax: python3 live.py <debug_mode> <resolution> <model_dir> <use_tflite>')
        print(' - <debug_mode> is either TRUE or FALSE')
        print(' - <resolution> is WidthXHeight (eg. 1280x960, 960x720, 640x480, 320x240)')
        print(' - <model_dir> is path to the Xiangpi predict model you wish to use')
        print(' - <use_tflite> is either TRUE or FALSE, suggesting it should use tflite model')
        exit(0)
    else:
        print('Pass "help" for more infomation on syntax')
        print('\n------------------------------------------------------------------\n')  
    
    if len(sys.argv) < 2: ## argv for <debug_mode> ######
        print('<debug_mode> defaults to False')
    else:
        DEBUG_MODE = (sys.argv[1].lower() == 'true')
        print('<debug_mode> is set to', DEBUG_MODE)
        
    if len(sys.argv) < 3: ## argv for <resolution> #####
        print('<resolution> defaults to 1280x640')
    else:
        try:
            st = sys.argv[2].lower()
            idx = st.find('x')
            RESOLUTION = (int(st[:idx]), int(st[idx+1:]))
        except Exception as e_parse:
            print('Error: Cannot parse resolution')
            print(e_parse)
        finally:
            print('<resolution> is set to', RESOLUTION)
    
    if len(sys.argv) < 4 or sys.argv[3] == '_': ## argv for <model_dir> ####
        MODEL_DIR = None
        print('<model_dir> is empty, is defaulted to what depends on <use_tfltie>')
    else:
        MODEL_DIR = sys.argv[3]
        print('<tf_model> is set to', MODEL_DIR)
    
    if len(sys.argv) < 5: ## argv for <use_tflite>
        print('<use_tflite> defaults to', USE_TFLITE)
    else:
        USE_TFLITE = (sys.argv[4].lower() == 'true')
        print('<use_tflite> is set to', USE_TFLITE)

    print('\n------------------------------------------------------------------\n')
    if MODEL_DIR is None:
        if USE_TFLITE: MODEL_DIR = DF_TFLMODEL_DIR
        else: MODEL_DIR = DF_TFMODEL_DIR
        print('<model_dir> is set to', MODEL_DIR, 'because <use_tflite> is set to', USE_TFLITE)
    print('\n------------------------------------------------------------------\n')

    print('Importing guesser libs and loading Tensorflow model...')
    global Guesser
    try:
        if USE_TFLITE:
            import TFLite_XiangpiGuesser as Guesser
        else:
            import XiangpiGuesser as Guesser
        Guesser.loadModel(MODEL_DIR)
    except Exception as e:
        print('FATAL: Cannot load Tensorflow model')
        print(e)
    else:
        print('Succeeded.')
    print('\n------------------------------------------------------------------\n')

####################################################################################################
##                                            WEB SERVER
####################################################################################################

## Camera, Streams
import io

## http servers
import socketserver
import threading
from http import server

## html headers
import mimetypes

APP_DIR = './Web/'

vp_thread = None

class StreamingHandler(server.BaseHTTPRequestHandler):
    def getByteObject(self, arr):
        img = Image.fromarray(arr.astype('uint8'))
        file_ob = io.BytesIO()
        img.save(file_ob, 'JPEG')
        file_ob.seek(0)
        return file_ob
    
    def writeFrame(self, frame):
        file_ob = self.getByteObject(frame)
        self.wfile.write(file_ob.getvalue())
        
    def writeMJPEGFrame(self, frame):
        self.wfile.write(b'--FRAME\r\n')
        file_ob = self.getByteObject(frame)
        self.send_header('Content-Type', 'image/jpeg')
        self.send_header('Content-Length', len(file_ob.getvalue()))
        self.end_headers()
        self.wfile.write(file_ob.getvalue())
        self.wfile.write(b'\r\n')
        
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path.startswith('/stream'):
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
        
            try:
                while True:
                    mut = [np.zeros((5,5,3), np.uint8)]
                    if self.path == '/stream_cam.mjpeg':
                        th = Thread(target=vpGet.threadsafe_getRawFrame, args=(mut,))
                        th.start(); th.join()
                        self.writeMJPEGFrame(mut[-1])
                    elif self.path == '/stream_mask.mjpeg':
                        th = Thread(target=vpGet.threadsafe_getMaskFrame, args=(mut,))
                        th.start(); th.join()
                        mask = cv2.cvtColor(mut[-1], cv2.COLOR_GRAY2RGB)
                        self.writeMJPEGFrame(mask)
                    elif self.path == '/stream_contour.mjpeg':
                        th = Thread(target=vpGet.threadsafe_getContourFrame, args=(mut,))
                        th.start(); th.join()
                        self.writeMJPEGFrame(mut[-1])
                    elif self.path == '/stream_canvas.mjpeg':
                        th = Thread(target=vpGet.threadsafe_getCanvasFrame, args=(mut,))
                        th.start(); th.join()
                        img = cv2.cvtColor(mut[-1], cv2.COLOR_RGBA2BGR)
                        self.writeMJPEGFrame(img)
            except Exception as e:
                print(e)
                #traceback.print_exc()
                logging.warning('Removed streaming client %s: %s', self.client_address, str(e))
            else:
                pass
        elif self.path == "/move_suggest_red.html":
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            prv = ''
            while True:
                try:
                    mut = ['.'*90]
                    th = Thread(target=vpGet.threadsafe_getDescriptorString, args=(mut,))
                    th.start(); th.join()
                    
                    if mut[-1] is None:
                        self.wfile.write(b'Board is not available yet, waiting 2s..<br>')
                        time.sleep(2)
                        continue
                    
                    if prv == mut[-1]:
                        time.sleep(1)
                        continue
                    
                    prv = mut[-1]
                    self.wfile.write(b'<br><br><br><br><br>')
                    self.wfile.write(b'<strong> Evaluating.. </strong> <br>')
                    chesspos = elephantfish.parseDescriptorToPos(prv)
                    
                    for move, score in elephantfish.getSuggestedMoves(chesspos):
                        st1 = move[0] + '-' + move[1]
                        st2 = str(score)
                        self.wfile.write((st1 + ' : ' + st2).encode())
                        
                        self.wfile.write(b'\r\n<br>')
                    self.wfile.write(b'<strong> Out of think time, finished eval.</strong>')
                    time.sleep(2)
                except Exception as e:
                    self.wfile.write(b'<p style="color: red; font-weight: bold"> Exception occur while launching engine </p>')
                    self.wfile.write(b'<br>')
                    self.wfile.write(str(e).encode())
                    self.wfile.write(b'\r\n')
                    break
        elif self.path == "/move_suggest_green.html":
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            prv = ''
            while True:
                try:
                    mut = ['.'*90]
                    th = Thread(target=vpGet.threadsafe_getDescriptorString, args=(mut,))
                    th.start(); th.join()
                
                    if mut[-1] is None:
                        self.wfile.write(b'Board is not available yet, waiting 2s..<br>')
                        time.sleep(2)
                        continue
                    if prv == mut[-1]:
                        time.sleep(2)
                        continue
                    
                    prv = mut[-1]
                    self.wfile.write(b'<br><br><br><br><br>')
                    self.wfile.write(b'<strong> Evaluating.. </strong> <br>')
                    chesspos = elephantfish.parseDescriptorToPos(prv)
                    
                    for move, score in elephantfish.getSuggestedMoves(chesspos, True):
                        st1 = move[0] + '-' + move[1]
                        st2 = str(score)                        
                        self.wfile.write((st1 + ' : ' + st2).encode())
                        self.wfile.write(b'\r\n<br>')
                    self.wfile.write(b'<strong> Out of think time, finished eval.</strong>')
                    time.sleep(2)
                except Exception as e:
                    self.wfile.write(b'<p style="color: red; font-weight: bold"> Exception occur while launching engine </p>')
                    self.wfile.write(b'<br>')
                    self.wfile.write(str(e).encode())
                    self.wfile.write(b'\r\n')
                    break
        else:
            try:
                idx = self.path.find('?')
                if idx > 0:
                    path = self.path[:idx]
                else:
                    path = self.path

                fpath = APP_DIR + path
                print(fpath)
                f = open(fpath, 'rb')
            except IOError:
                self.send_error(404, 'File not found: %s' % fpath)
            else:
                self.send_response(200)
                mimetype, _ = mimetypes.guess_type(fpath)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == '__main__':
    preload()
    try:
        print('Creating Video processing thread..')
        vp_thread = VideoProcessor('processor', preprocess, XiangpiRender, Guesser, RESOLUTION, 12)
        vp_thread.start()
        print('Succeed.\n\n')
    except:
        print('FATAL: Failed to start the VP_Thread.')
        raise
    
    try:
        print('Starting the server.')
        print('------------------------------------------------------------------\n')  
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    except Exception as e:
        print('Failed to start the server..')
        print(e)
        traceback.print_exc()
    finally:
        pass
