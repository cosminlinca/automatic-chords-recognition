import random

import keras
import numpy as np
from keras.layers import Activation, Dense, Dropout, Conv2D, Flatten, MaxPooling2D
from keras.models import Sequential

from science import utils as AUDIO_CONSTANTS


def train():
    # Load computed dataset from .npy file
    dataset = np.load(AUDIO_CONSTANTS.RESOURCES_PATH + "//models//data_chroma24_hop512_beta_V3.npy", allow_pickle=True)
    random.shuffle(dataset)

    # Split dataset in training/testing
    training_dataset = dataset[:48000]
    testing_dataset = dataset[48000:]

    print("Training size: " + str(len(training_dataset)))
    print("Testing size:  " + str(len(testing_dataset)))

    X_train, Y_train = zip(*training_dataset)
    X_test, Y_test = zip(*testing_dataset)
    print(X_train[0].shape)

    # Reshape for CNN input
    X_train = np.array([x.reshape((24, 87, 1)) for x in X_train])
    X_test = np.array([x.reshape((24, 87, 1)) for x in X_test])
    print(X_train[0].shape)

    # One-Hot encoding for classes
    Y_train = np.array(keras.utils.to_categorical(Y_train, 25))
    Y_test_values = Y_test
    Y_test = np.array(keras.utils.to_categorical(Y_test, 25))

    print(Y_train[0])

    # Compute CNN model
    model = Sequential()
    input_shape = (24, 87, 1)

    model.add(Conv2D(24, (2, 2), input_shape=input_shape))
    model.add(MaxPooling2D())
    model.add(Activation('relu'))

    model.add(Conv2D(32, (2, 2), padding="valid"))
    model.add(Activation('relu'))

    model.add(Flatten())
    model.add(Dropout(rate=0.5))

    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(rate=0.5))

    model.add(Dense(25))
    model.add(Activation('softmax'))

    model.summary()

    model.compile(
        optimizer="Adam",
        loss="categorical_crossentropy",
        metrics=['accuracy'])

    model.fit(
        x=X_train,
        y=Y_train,
        epochs=25,
        validation_data=(X_test, Y_test))

    score = model.evaluate(
        x=X_test,
        y=Y_test)

    print('Test accuracy:', score[1])

    predictions = model.predict_classes(X_test)
    predictions

    Y_test_values = np.array(Y_test_values)
    Y_test_values

    model.save(AUDIO_CONSTANTS.RESOURCES_PATH + "//model_beta_chroma24_hop512_25epochs.h5")
    print("Model evaluation is done...Please check the results!")


train()
