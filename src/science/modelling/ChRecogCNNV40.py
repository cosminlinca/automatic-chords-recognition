import datetime
import logging
import os
import matplotlib.pyplot as plt
import keras
from keras.callbacks import EarlyStopping
from keras.layers import Activation, Dense, Dropout, Conv2D, MaxPooling2D, BatchNormalization, \
    Flatten
from keras.models import Sequential
from sklearn.metrics import confusion_matrix

from science.modelling.CNNInterface import CNNInterface
from science.utils import constants as AUDIO_CONSTANTS
from science.utils.logging import logging_setup
from science.utils.metrics import *

# Custom logging
logging_setup()
# Use logging system
logger = logging.getLogger('src.modelling.ChRecogCNNV40')


class ChRecogCNN40(CNNInterface):

    def __init__(self, name, input_shape):
        self.__input_shape = input_shape
        self.__name = name
        self.__score_train = []
        self.__score_test = []
        self.__history = None

        logger.info("Initializing CNN")
        logger.info(f"Input shape = {self.__input_shape}")
        self.__model = Sequential()

        self.__model.add(Conv2D(24, (3, 3), input_shape=input_shape))
        self.__model.add(BatchNormalization())
        self.__model.add(MaxPooling2D())
        self.__model.add(Activation('relu'))

        self.__model.add(Conv2D(48, (3, 3), padding="valid"))
        self.__model.add(BatchNormalization())
        self.__model.add(MaxPooling2D())
        self.__model.add(Activation('relu'))

        self.__model.add(Conv2D(48, (3, 3), padding="valid"))
        self.__model.add(Activation('relu'))

        self.__model.add(Flatten())
        self.__model.add(Dropout(rate=0.5))

        self.__model.add(Dense(128))
        self.__model.add(Activation('relu'))
        self.__model.add(Dropout(rate=0.5))

        self.__model.add(Dense(25))
        self.__model.add(Activation('softmax'))

        logger.info("CNN Initialized")

    def __str__(self):
        return str(self.__model.summary())

    def train(self, X_train, Y_train, X_test, Y_test):
        logger.info("Start training model")

        self.__model.compile(
            optimizer="Adam",
            loss="categorical_crossentropy",
            metrics=['accuracy', precision, recall, f1measure])

        # TensorBoard Logging
        log_dir = os.path.join(AUDIO_CONSTANTS.LOGGING_PATH, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

        logger.info("Tensorboard Logging Started")
        logger.info("Use the following command in the terminal to view the logs during training: tensorboard --logdir "
                    "logs/training")

        self.__history = self.__model.fit(
            x=X_train,
            y=Y_train,
            epochs=30,
            batch_size=64,
            validation_data=(X_test, Y_test),
            callbacks=[tensorboard_callback,
                       EarlyStopping(monitor='val_loss', verbose=1, patience=1)])

        logger.info("Training completed")

    def evaluate(self, X_train, Y_train, X_test, Y_test):
        self.__score_train = self.__model.evaluate(
            x=X_train,
            y=Y_train)

        self.__score_test = self.__model.evaluate(
            x=X_test,
            y=Y_test)

        logger.info(f'Train loss: {self.__score_train[0]}')
        logger.info(f'Train accuracy: {self.__score_train[1]}')
        logger.info(f'Train precision: {self.__score_train[2]}')
        logger.info(f'Train recall: {self.__score_train[3]}')
        logger.info(f'Train f1-score: {self.__score_train[4]}')

        logger.info(f'Test loss: {self.__score_test[0]}')
        logger.info(f'Test accuracy: {self.__score_test[1]}')
        logger.info(f'Test precision: {self.__score_test[2]}')
        logger.info(f'Test recall: {self.__score_test[3]}')
        logger.info(f'Test f1-score: {self.__score_test[4]}')

    def save_model(self):
        logger.info("Saving model")
        model_path = AUDIO_CONSTANTS.RESOURCES_PATH + "//" + self.__name + ".h5"
        self.__model.save(model_path)
        logger.info("Model saved to " + model_path)

    def confusion_matrix(self, X_test, Y_test_values):
        y_pred = self.__model.predict_classes(X_test)
        conf_matrix = confusion_matrix(Y_test_values, y_pred, labels=range(25))
        logger.info('Confusion Matrix \n{}'.format(conf_matrix))

    def plot_history(self):
        if self.__history is not None:
            # Summarize history for accuracy
            plt.plot(self.__history.history['accuracy'])
            plt.plot(self.__history.history['val_accuracy'])
            plt.title('model accuracy')
            plt.ylabel('accuracy')
            plt.xlabel('epoch')
            plt.legend(['train', 'test'], loc='upper left')
            plt.show()

            # Summarize history for loss
            plt.plot(self.__history.history['loss'])
            plt.plot(self.__history.history['val_loss'])
            plt.title('model loss')
            plt.ylabel('loss')
            plt.xlabel('epoch')
            plt.legend(['train', 'test'], loc='upper left')
            plt.show()
