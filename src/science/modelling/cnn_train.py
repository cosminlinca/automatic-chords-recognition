import logging
import numpy as np
import random
import keras

from science.utils import constants as AUDIO_CONSTANTS

from science.modelling.ChRecogCNNV2 import ChRecogCNNV2
from science.modelling.ChRecogCNNV30 import ChRecogCNNV30
from science.modelling.ChRecogCNN import ChRecogCNN
from science.modelling.ChRecogCNNV22 import ChRecogCNNV22
from science.modelling.ChRecogCNNV32 import ChRecogCNNV32
from science.modelling.ChRecogCNNV40 import ChRecogCNN40

from science.utils.logging import logging_setup

logging_setup()
logger = logging.getLogger('src.modelling.cnn_train')


def split_dataset(dataset, split_ratio=0.80):
    logger.info(f"Dataset size: {len(dataset)}")
    logger.info(f"Split dataset with split ratio: {split_ratio}")
    random.shuffle(dataset)

    limit = round(len(dataset) * split_ratio)
    train_data = dataset[:limit]
    test_data = dataset[limit:]

    logger.info(f"Number of training samples is {len(train_data)}")
    logger.info(f"Number of testing samples is {len(test_data)}")
    logger.info(f"Train-Test split completed")

    return train_data, test_data


def main():
    logger.info("Start Training Process")

    # Load computed dataset from .npy file
    dataset = np.load(AUDIO_CONSTANTS.RESOURCES_PATH + "//models//data_chroma24_hop512_new_distribution_0905.npy"
                      , allow_pickle=True)
    training_dataset, testing_dataset = split_dataset(dataset)

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
    ch_recog_cnn = ChRecogCNN("model_ChRecogCNN_DatasetModified", input_shape)
    logger.info(ch_recog_cnn)

    ch_recog_cnn.train(X_train, Y_train, X_test, Y_test)
    ch_recog_cnn.evaluate(X_train, Y_train, X_test, Y_test)
    ch_recog_cnn.save_model()
    ch_recog_cnn.confusion_matrix(X_test, Y_test_values)
    ch_recog_cnn.plot_history()


if __name__ == '__main__':
    main()
