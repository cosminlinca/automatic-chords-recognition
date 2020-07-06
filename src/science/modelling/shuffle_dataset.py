import numpy as np
from science.utils import constants as AUDIO_CONSTANTS
import random

# Load computed dataset from .npy file
dataset = np.load(AUDIO_CONSTANTS.RESOURCES_PATH + "//models//data_chroma24_hop512_new_distribution_0905.npy"
                  , allow_pickle=True)
print(dataset[:5])

random.shuffle(dataset)

print("Dataset after shuffle")
print(dataset[:5])
np.save(AUDIO_CONSTANTS.RESOURCES_PATH +
        "//data_chroma24_hop512_new_distribution_shuffled_2705.npy", dataset)
print("Shuffle is done")