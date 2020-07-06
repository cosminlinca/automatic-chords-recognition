import os
import librosa
import numpy as np
from science.utils import constants as AUDIO_CONSTANTS


def noise_injection(rootDatasetPath, destinationDatasetPath):
    root_directories = os.listdir(rootDatasetPath)
    for childDir in root_directories:
        child_files = os.listdir(rootDatasetPath + "//" + childDir)
        for childFile in child_files:
            print(rootDatasetPath + "//" + childDir + "//" + childFile)
            file_absolute_path = rootDatasetPath + "//" + childDir + "//" + childFile
            song, sr = librosa.load(file_absolute_path)

            # Noise injection
            rate = 0.0075
            song_with_noise = song.copy()
            noise_amp = rate * np.random.uniform() * np.amax(song_with_noise)
            song_with_noise = song_with_noise.astype('float64') + noise_amp * np.random.normal(
                size=song_with_noise.shape[0])

            librosa.output.write_wav(
                destinationDatasetPath + "//" + childDir + "//" + childFile + '_with_noise_' + str(
                    int(rate * 1000)) + ".wav", song_with_noise, sr)


def change_speed(rootDatasetPath, destinationDatasetPath, rate):
    root_directories = os.listdir(rootDatasetPath)
    for childDir in root_directories:
        child_files = os.listdir(rootDatasetPath + "//" + childDir)
        for childFile in child_files:
            print(rootDatasetPath + "//" + childDir + "//" + childFile)
            file_absolute_path = rootDatasetPath + "//" + childDir + "//" + childFile
            song, sr = librosa.load(file_absolute_path)
            augmented_song = librosa.effects.time_stretch(song, rate=rate)

            librosa.output.write_wav(
                destinationDatasetPath + "//" + childDir + "//" + childFile + '_speed_055' + ".wav", augmented_song, sr)


# print(noise_injection(AUDIO_CONSTANTS.AUXILIARY_DATASET,
#                       AUDIO_CONSTANTS.AUXILIARY_DATASET_AUGMENTED))

print(change_speed(AUDIO_CONSTANTS.AUXILIARY_DATASET,
                   AUDIO_CONSTANTS.AUXILIARY_DATASET_AUGMENTED,
                   0.55))
