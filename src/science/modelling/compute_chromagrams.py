import threading

import librosa
import librosa.display
import numpy as np
import pandas as pd

from science.utils import constants as AUDIO_CONSTANTS
processed_data = []


# Define processing thread
class ChromaProcessingThread(threading.Thread):
    def __init__(self, threadID, name, start_point, stop, data_labeled):
        threading.Thread.__init__(self)
        self.__threadID = threadID
        self.__name = name
        self.__start_point = start_point
        self.__stop = stop
        self.__data_labeled = data_labeled

    def run(self):
        print("Starting " + self.__name + "/n")

        for i in range(self.__start_point, self.__stop):
            # print (str(self.threadID) + " " + str(i))
            # print(data_labeled.loc[i].path)
            song, sr = librosa.load(self.__data_labeled.loc[i].file_name, duration=2)
            chromagram = librosa.feature.chroma_cqt(song, sr=sr, hop_length=AUDIO_CONSTANTS.hop_length, n_chroma=24,
                                                    n_octaves=7)

            # chromagram = librosa.feature.melspectrogram(song, sr=sr)
            # chromagram = librosa.feature.chroma_stft(song, sr=sr, hop_length = hop_length, n_chroma=24)
            # np.reshape(chromagram, (24, 87))

            aux_chroma = []
            if chromagram.shape != (24, 87):
                for row in chromagram:
                    while len(row) < 87:
                        # print(len(row))
                        row = np.append(row, [0])

                    aux_chroma.append(row)
                chromagram = np.array(aux_chroma)

            # np.reshape(chromagram, (24, 87))
            # print(chromagram.size)
            processed_data.append((chromagram, self.__data_labeled.loc[i].classID))

        print("Exiting /n" + self.__name + "/n")


# #---------------------------------------------------------------------------------------------------------------------------

### MAIN

def compute():
    # Labeled data
    data_labeled = pd.read_excel(AUDIO_CONSTANTS.RESOURCES_PATH + "//pandas_chords_modified.xlsx")
    # data_labeled['path'] =  data_labeled['classname'].astype('str') + '/' + data_labeled['file_name'].astype('str')
    print(data_labeled)

    threads = []
    start_point = 0
    stop = 5947
    for i in range(1, 11):
        thread = ChromaProcessingThread(i, "Thread " + str(i), start_point, stop, data_labeled)
        thread.start()
        threads.append(thread)
        if i <= 9:
            start_point = stop
            stop += 5947

    for i in range(0, 10):
        threads[i].join()

    print(len(processed_data))
    np.save(AUDIO_CONSTANTS.RESOURCES_PATH +
            "//data_chroma24_hop512_new_distribution_0905.npy", processed_data)


compute()
