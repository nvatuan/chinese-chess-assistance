import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential 

data_dir = "./Dataset"
batch_size = 32
IMAGE_HEIGHT = 50
IMAGE_WIDTH = 50

CATEGORIES = ['Chuot Den', 'Chuot Do', 'Empty', 'Ma Den', 'Ma Do', 'Phao Den', 'Phao Do', 'Si Den', 'Si Do', 'Tinh Den', 'Tinh Do', 'Tuong Den', 'Tuong Do', 'Xe Den', 'Xe Do']
DIR = '..\\Dataset'

def loading_from_directory(DIR, CATEGO, IMG_DIM = (IMAGE_HEIGHT, IMAGE_WIDTH)):
    x, y = [], []

    import os
    import cv2
    from tqdm import tqdm
    for catego in CATEGO:
        path = os.path.join(DIR, catego)
        print('Loading from', path)
        class_no = CATEGO.index(catego)

        for img in tqdm(os.listdir(path), ncols=50):
            img_arr = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
            img_arr = cv2.resize(img_arr, IMG_DIM, cv2.INTER_CUBIC)

            x.append(img_arr)
            y.append(class_no)
        
        print('Finished loading from', path)
    return x, y

def train_test_from_dataset(x_ds, y_ds, split_ratio = 0.7):
    assert (len(x_ds) == len(y_ds)), "Missing labels or dataset"
    indices = list(range(len(x_ds)))

    from random import shuffle 
    shuffle(indices)
    
    training_indices = set()
    for i in range(int(len(x_ds) * split_ratio)):
        training_indices.add(indices[i])

    x_train, y_train, x_test, y_test = [], [], [], []
    for i in range(len(x_ds)):
        if i in training_indices:
            x_train.append(x_ds[i])
            y_train.append(y_ds[i])
        else:
            x_test.append(x_ds[i])
            y_test.append(y_ds[i])
    return np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)

def show_9_samples(x, y):
    import matplotlib.pyplot as plt
    import numpy as np 

    fig, ax = plt.subplots(3, 3, figsize=(10, 10))
    for i in range(3):
        for j in range(3):
            s = np.random.randint(0, len(x))
            val = x[s]
            img = val.reshape(IMAGE_HEIGHT, IMAGE_WIDTH)
            ax[i][j].imshow(img)
            ax[i][j].set_title(CATEGORIES[y[s]], fontsize=16)
    plt.show()

def build_model():
    model = Sequential([
        layers.experimental.preprocessing.Rescaling(1./255, input_shape=(IMAGE_HEIGHT, IMAGE_WIDTH, 1)),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(128, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(256, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.2),
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.Dense(len(CATEGORIES))
    ])
    model.compile(optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
    return model

def rotate_generator(x, y):
    n = len(x)
    print(' GEN @ Appending 90/180/270-Rotated version of each sample...')
    from tqdm import tqdm
    for idx in tqdm(range(n), ncols=50):
        img = x[idx].copy()
        for i in range(3):
            img = np.rot90(img)
            x = np.append(x, np.array([img]), axis=0)
            y = np.append(y, np.array([y[idx]]))
    
    return x, y

def brightness_generator(x, y, COPIES=10, BR_RANGE = (-100, 100)):
    import numpy as np
    BRs = []
    mid = (BR_RANGE[1] - BR_RANGE[0])//2
    for i in range(BR_RANGE[0] + np.random.randint(0, 10), BR_RANGE[1]+1, np.random.randint(1, 14)):
        cnt = i**2 // 300
        BRs = BRs + [i]*cnt

    n = len(x)

    print(' GEN @ Adding random brightness to each sample...')
    from tqdm import tqdm
    import random
    import cv2

    for idx in tqdm(range(n), ncols=50):
        img, lbl = x[idx].copy(), y[idx].copy()

        for cc in range(COPIES):
            br = random.choice(BRs)
            brImg = cv2.add(img, np.array([float(br)]))
            x = np.append(x, np.array([brImg]), axis=0)
            y = np.append(y, np.array([lbl]))
    
    return x, y


if __name__ == "__main__":
    x_ds, y_ds = loading_from_directory(DIR, CATEGORIES)
    print('Dataset\'s size:', len(x_ds))

    # ================= self-written generator
    #x_ds, y_ds = rotate_generator(x_ds, y_ds)
    #x_ds, y_ds = brightness_generator(x_ds, y_ds)
    print('Dataset\'s size after generate:', len(x_ds))

    # ================ self-written splitter
    x_train, y_train, x_val, y_val = train_test_from_dataset(x_ds, y_ds, 0.8)
    print('Training set\'s size:', len(x_train))
    print('Test\'s size:', len(x_val))

    # ================= model

    model = build_model()
    model.summary()
    exit(0)

    # ================= checkpointing
    # outputFolder = './checks'
    # if not os.path.exists(outputFolder):
    #     os.makedirs(outputFolder)
    # filepath=outputFolder+"/modelG-augDs-{epoch:02d}-{val_accuracy:.2f}"

    # from tensorflow.keras.callbacks import ModelCheckpoint
    # checkpoint_callback = ModelCheckpoint(
    #     filepath, monitor='val_accuracy', verbose=1,
    #     save_best_only=False, save_weights_only=False,
    #     save_freq='epoch', period=200
    # )

    # ================= training
    EPOCHS=50
    history = model.fit(
        x_train,
        y_train,
        batch_size=32,
        #callbacks=[checkpoint_callback],
        epochs=EPOCHS,
        validation_data=(x_val, y_val),
    )

    # ================= plotting accuracy
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(EPOCHS)

    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    
    MODELNAME = "graph20epoch-28Dec20" 
    plt.savefig('fig_' + MODELNAME + '.png', bbox_inches='tight')
    model.save(MODELNAME + '.model')