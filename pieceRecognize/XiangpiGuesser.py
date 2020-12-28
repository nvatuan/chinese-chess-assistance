import numpy as np
import tensorflow as tf
import cv2

model = None

def loadModel(modelName = "Xiangpi.model"):
    global model
    model = tf.keras.models.load_model(modelName)
    return model

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
    if model is None:
        loadModel()
    
    img = np.asarray(img)
    if (len(img.shape) > 2):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.resize(img, IMAGE_DIM)
    img = img.reshape((1, IMAGE_DIM[0], IMAGE_DIM[1], 1))

    prediction = model.predict(img)
    return getLabelFromOutput(np.argmax(prediction), oneLetterMode)

def guessFile(filename):
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    return guess(img)

if __name__ == "__main__":
    import matplotlib.pyplot as plt 
    import cv2
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

    model = loadModel("./models/G_augDs_1.5mil-param_1000epch")

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