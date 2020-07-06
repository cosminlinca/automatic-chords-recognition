import logging
import keras

import numpy as np
from keras.models import load_model
from sklearn.metrics import confusion_matrix

from science.utils import constants as AUDIO_CONSTANTS
from science.modelling import cnn_train as CNN_Train
from science.utils.logging import logging_setup
from science.utils.metrics import *

logging_setup()
logger = logging.getLogger('src.model_evaluation.confusion_matrix')

model = load_model(AUDIO_CONSTANTS.RESOURCES_PATH +
                   "//model_output" + "//model_V2_2_ChordsRecognition_ConvNet_85.h5",
                   custom_objects={'precision': precision, 'recall': recall, 'f1measure': f1measure})

# Load computed dataset from .npy file
dataset = np.load(AUDIO_CONSTANTS.RESOURCES_PATH + "//models//data_chroma24_hop512_beta_V3.npy", allow_pickle=True)
training_dataset, testing_dataset = CNN_Train.split_dataset(dataset)

X_train, Y_train = zip(*training_dataset)
X_test, Y_test = zip(*testing_dataset)

# Reshape for CNN input
X_train = np.array([x.reshape((24, 87, 1)) for x in X_train])
X_test = np.array([x.reshape((24, 87, 1)) for x in X_test])
# logging.info("Shape " + str(X_train[0].shape))

# One-Hot encoding for classes
Y_train = np.array(keras.utils.to_categorical(Y_train, 25))
Y_test_values = Y_test
Y_test = np.array(keras.utils.to_categorical(Y_test, 25))

y_pred = model.predict_classes(X_test)
conf_matrix = confusion_matrix(Y_test_values, y_pred, labels=range(25))
logger.info('Confusion Matrix \n{}'.format(conf_matrix))
