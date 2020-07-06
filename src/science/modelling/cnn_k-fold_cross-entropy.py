import logging

import keras
import numpy as np

from science.modelling.ChRecogCNN import ChRecogCNN
from science.utils import constants as AUDIO_CONSTANTS
from science.utils.logging import logging_setup

logging_setup()
logger = logging.getLogger('src.modelling.cnn_k-fold_cross-entropy')


def main():
    logger.info("Resampling Method using k-fold Cross Validation")

    # Load computed dataset from .npy file
    dataset = np.load(AUDIO_CONSTANTS.RESOURCES_PATH +
                      "//models//data_chroma24_hop512_new_distribution_shuffled_2705.npy"
                      , allow_pickle=True)
    training_results = []
    testing_results = []

    interval_length = int(len(dataset) / 5)
    start = 0
    stop = interval_length
    print("Start and stop, interval points")
    print(str(start) + "-" + str(stop))

    i = 0
    logger.info("kFold Step " + str(i))
    if i == 0:
        testing_dataset = dataset[start:stop]
        training_dataset = dataset[stop:]
    elif i == 4:
        testing_dataset = dataset[start:stop]
        training_dataset = dataset[:start]
    else:
        testing_dataset = dataset[start:stop]
        training_dataset = list(dataset[:start]) + list(dataset[stop:])
        # training_dataset = np.array(training_dataset)

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

    input_shape = (24, 87, 1)
    ch_recog_cnn = ChRecogCNN("model_ChRecogCNN_kFold_" + str(i), input_shape)
    logger.info(ch_recog_cnn)

    ch_recog_cnn.train(X_train, Y_train, X_test, Y_test)
    [score_train, score_test] = ch_recog_cnn.evaluate(X_train, Y_train, X_test, Y_test)
    ch_recog_cnn.save_model()

    training_results.append(score_train)
    testing_results.append(score_test)
    # ch_recog_cnn.confusion_matrix(X_test, Y_test_values)
    # ch_recog_cnn.plot_history()


if __name__ == '__main__':
    main()
