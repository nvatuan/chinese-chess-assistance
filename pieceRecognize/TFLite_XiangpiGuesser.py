import numpy as np
import tensorflow as tf 
import cv2

interpreter = None
input_details = None
output_details = None

def pprint_interpreter():
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(input_details)
    pp.pprint(output_details)

def loadModel(modelName = "Xiangpi.tflite"):
    global interpreter, input_details, output_details
    try:
        interpreter = tf.lite.Interpreter(model_path = modelName)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        return True
    except Exception as e:
        print('Error: Cannot load tflite interpreter')
        print(e)
        return False

CATEGORIES = ['bc', 'rc', '-', 'bm', 'rm', 'bp', 'rp', 'bs', 'rs', 'bt', 'rt', 'bg', 'rg', 'bx', 'rx']
classes = {}
for i in range(len(CATEGORIES)):
    classes[i] = CATEGORIES[i]
    classes[CATEGORIES[i]] = i

def getLabelFromOutput(output, oneLetterMode = False):
    global CATEGORIES, classes
    ret = classes.get(output, None)
    if ret is None: return None
    if ret == '-': return '-'
    if oneLetterMode: return (ret[1].upper() if ret[0] == 'r' else ret[1])
    return ret

def guess(img, oneLetterMode=False, IMAGE_DIM=(50, 50)):
    global interpreter, input_details, output_details
    if interpreter is None:
        loadInterpreter()

    if (len(img.shape) > 2):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.resize(img, IMAGE_DIM, interpolation=cv2.INTER_CUBIC)
    
    img = img.reshape(input_details[0]['shape'])
    img = img.astype(np.float32)

    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    return (getLabelFromOutput(np.argmax(output), oneLetterMode))

def guessFile(filename):
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    return guess(img)

if __name__ == "__main__":
    loadInterpreter('./model.tflite')

    import matplotlib.pyplot as plt
    import os
    GUESS_DIR = "./Guessing"
    GuessList = os.listdir(GUESS_DIR)

    from math import sqrt, ceil
    side = int(ceil(sqrt(len(GuessList))))
    fig, ax = plt.subplots(side, side, figsize=(10, 10))

    fig.suptitle('Testing the model with a separate guess dataset')

    for idx in range(side):
        for jdx in range(side):
            ax[idx][jdx].axis('off')
    for idx, g in enumerate(GuessList):
        G = guessFile(GUESS_DIR + '/' + g)
        #print("I guess:", G)
        #print("Answer:", g.split('.')[0])

        img_rgb = plt.imread(GUESS_DIR+'/'+g) 

        ax[idx//side][idx%side].imshow(img_rgb)
        ax[idx//side][idx%side].set_title("" + G + " (ans: " + g.split('.')[0] + ")", fontsize=10)
    fig.tight_layout()
    plt.show()