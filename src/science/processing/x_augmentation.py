#
# Data augmentation module
# - Changing Speed
# - Noise injection
#


import threading
import librosa
import pandas as pd
import librosa.display
import numpy as np
from science import utils as AUDIO_CONSTANTS


# Define my processing thread
class ProcessingThread(threading.Thread):
    def __init__(self, threadID, name, start_point, stop):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.start_point = start_point
        self.stop = stop

    def run(self):
        print("Starting " + self.name + "/n")

        for i in range(self.start_point, self.stop):
            print(data_labeled.loc[i].path)
            song, sr = librosa.load(AUDIO_CONSTANTS.DATASET_PATH + "//jams_audio" + "//" + data_labeled.loc[i].path,
                                    duration=2)
            # chromagram = librosa.feature.chroma_cqt(song, sr=sr, hop_length = hop_length, n_chroma=24, n_octaves=7)
            ## Changing speed
            # song_changed = librosa.effects.time_stretch(song, rate=rate)

            # Noise injection
            rate = 0.005
            song_with_noise = song.copy()
            noise_amp = rate * np.random.uniform() * np.amax(song_with_noise)
            song_with_noise = song_with_noise.astype('float64') + noise_amp * np.random.normal(
                size=song_with_noise.shape[0])

            librosa.output.write_wav(
                AUDIO_CONSTANTS.DATASET_PATH + "//augmented" + "//" + data_labeled.loc[i].path + '_with_noise_' + str(
                    int(rate * 1000)) + ".wav", song_with_noise, sr)

        print("Exiting /n" + self.name + "/n")


# ---------------------------------------------------------------------------------------------------------------------------

# Read labeled excel
data_labeled = pd.read_excel(AUDIO_CONSTANTS.RESOURCES_PATH + "//pandas_chords.xlsx")
data_labeled['path'] = data_labeled['classname'].astype('str') + '/' + data_labeled['file_name'].astype('str')
print(data_labeled)

#  I) Changing Speed
## 1. Speed up by 1.07/1.25
## 2. Speed down by 0.75
# rate = 0.75

#  II) Noise Injection - rate: 0.005

# Thread locking object
# threadLock = threading.Lock()
# threads = []

# start_point = 0
# stop = 335
# for i in range(1, 11):
#     thread = ProcessingThread(i, "Thread " + str(i), start_point, stop)
#     thread.start()
#     threads.append(thread)
#     if(i <= 9):
#         start_point = stop
#         stop += 335

# for i in range(0, 10):
#     threads[i].join()
