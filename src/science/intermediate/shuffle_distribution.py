import os
import random
from science.utils import constants as AUDIO_CONSTANTS
from shutil import copyfile, copy

location = "//auxiliary_dataset_augmented//n"
original_files = os.listdir(AUDIO_CONSTANTS.DATASET_PATH + location)
destination_file_path = AUDIO_CONSTANTS.DATASET_MODIFIED_PATH + location

split_ratio = 0.20
random.shuffle(original_files)
limit = round(len(original_files) * split_ratio)
print(limit)
print(original_files[0])

for i in range(0, limit):
    copy(AUDIO_CONSTANTS.DATASET_PATH + location + "//" + original_files[i],
         destination_file_path)

print("Finished")
