from keras.models import load_model
from science.utils.metrics import *
from science import utils as AUDIO_CONSTANTS
import librosa.display
import numpy as np


class ChordPrediction:
    """
        Predict a chord using loaded model

        :parameter audio_file: .wav file - representing the audio input file, which is a simple chord
        :return: [int]: a prediction value
    """

    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.model = load_model(AUDIO_CONSTANTS.RESOURCES_PATH +
                                "//model_output" + "//model_V2_2_ChordsRecognition_ConvNet_85.h5",
                                custom_objects={'precision': precision, 'recall': recall, 'f1measure': f1measure})

        song, sr = librosa.load(self.audio_file, duration=2)

        # Compute chromagram using Constant-Q transformation
        chromagram = librosa.feature.chroma_cqt(song, sr=sr, hop_length=AUDIO_CONSTANTS.hop_length, n_chroma=24,
                                                n_octaves=7)

        # Add 0 to np.array representation if the shape is not standard
        aux_chroma = []
        if chromagram.shape != (24, 87):
            for row in chromagram:
                while len(row) < 87:
                    row = np.append(row, [0])

                aux_chroma.append(row)
            chromagram = np.array(aux_chroma)

        chromagram = chromagram.reshape((24, 87, 1))

        self.chroma = chromagram

    def predict_proba(self):
        # Return prediction using loaded model
        return self.model.predict_proba(np.array([self.chroma]))

    def predict_classes(self):
        # Return prediction using loaded model
        return self.model.predict_classes(np.array([self.chroma]))
