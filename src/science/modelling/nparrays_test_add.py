import numpy as np
from science.utils import constants as AUDIO_CONSTANTS

dataset = np.load(AUDIO_CONSTANTS.RESOURCES_PATH + "//models//data_chroma24_hop512_new_distribution_0905.npy"
                  , allow_pickle=True)

start = 500
stop = 5000

# Fix for cnn_k-fold_cross-entropy.py
array_t = list(dataset[:start]) + list(dataset[stop:])
array_t = np.array(array_t)

print(array_t.shape)
print(len(array_t))

