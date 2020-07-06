import librosa
from keras.models import load_model
from science.utils.metrics import *
from science.model_evaluation.entities.DetectionType import DetectionType

import numpy as np
from science.utils import constants as AUDIO_CONSTANTS


class OnsetClassify:
    """
        Parameters
        ---------
        :parameter audio_file -  Audio file content
        :parameter beta_length - Minor length for measurable input sample

        Return
        ------
        {
           [
                 {
                      "Pitch_start": "",
                      "Duration": "",
                      "Predictions": [
                                       { "Chord": "", "Probability": "" },
                                       ...
                                     ]
                 },
                         ...
            ]
        }
    """

    def __init__(self, audio_file_path, beta_length):
        self.__audio_file_path = audio_file_path
        self.__beta_length = beta_length

        self.__model = load_model(AUDIO_CONSTANTS.RESOURCES_PATH +
                                  "//model_output" + "//model_ChRecogCNN_DatasetModified.h5",
                                  custom_objects={'precision': precision, 'recall': recall, 'f1measure': f1measure})

        # self.__model.summary()
        song, sr = librosa.load(self.__audio_file_path)
        self.__duration = librosa.get_duration(y=song, sr=sr)
        if self.__duration <= 2:
            self.__detection_type = DetectionType.CHORD_PREDICTION
        else:
            self.__detection_type = DetectionType.ONSET_DETECTION

        self.__audio_time_series = song
        self.__sampling_rate = sr
        self.__onset_times = None

    def predict(self):
        if self.__detection_type == DetectionType.CHORD_PREDICTION:
            # Compute chromagram using Constant-Q transformation
            print("Sound processing started...")
            chroma = librosa.feature.chroma_cqt(self.__audio_time_series, sr=self.__sampling_rate,
                                                hop_length=AUDIO_CONSTANTS.hop_length, n_chroma=24,
                                                n_octaves=7)

            # Add 0 to np.array representation if the shape is not standard
            aux_chroma = []
            if chroma.shape != (24, 87):
                for row in chroma:
                    while len(row) < 87:
                        row = np.append(row, [0])

                    aux_chroma.append(row)
                chroma = np.array(aux_chroma)

            chroma = chroma.reshape((24, 87, 1))

            probabilities_prediction = self.__model.predict_proba(np.array([chroma]))
            np_prediction = np.array(probabilities_prediction)
            predictions = []
            onsets = []

            ids = (-np_prediction).argsort()[:3][0][:3]
            for prediction_id in ids:
                for chord, value in AUDIO_CONSTANTS.CLASS_MAPPER.items():
                    if value == prediction_id:
                        predictions.append(dict({"Chord": chord,
                                                 "Probability": '{0:.10f}'.format(np_prediction[0][prediction_id])}))

            response = ({"Pitch_start": 0, "Duration": self.__duration, "Predictions": predictions})
            onsets.append(response)

            print("Sound processing finished.")
            return onsets

        else:
            # Obtain onset frames
            print("Sound processing started...")
            onset_frames = librosa.onset.onset_detect(self.__audio_time_series,
                                                      sr=self.__sampling_rate, backtrack=True)
            self.__onset_times = librosa.frames_to_time(onset_frames)

            onsets = []
            i = 0
            while i < (len(self.__onset_times) - 1):
                offsetValue = self.__onset_times[i]
                diff = self.__onset_times[i + 1] - offsetValue

                while diff < self.__beta_length and i < (len(self.__onset_times) - 1):
                    diff = self.__onset_times[i + 1] - offsetValue
                    i = i + 1

                # Chroma superior limit
                if diff > 2:
                    x = diff - 2
                    diff = diff - x

                # Load audio using computed offset
                song, sr = librosa.load(self.__audio_file_path,
                                        offset=offsetValue, duration=diff)

                # Compute chroma
                chroma = librosa.feature.chroma_cqt(song, sr=sr,
                                                    hop_length=AUDIO_CONSTANTS.hop_length,
                                                    n_chroma=24,
                                                    n_octaves=7)

                # Add white noise as 0 value, if computed chroma does not have standard shape
                aux_chroma = []
                if chroma.shape < (24, 87):
                    for row in chroma:
                        while len(row) < 87:
                            row = np.append(row, [0])

                        aux_chroma.append(row)
                    chroma = np.array(aux_chroma)

                i = i + 1

                # Reshape chroma
                chroma = chroma.reshape((24, 87, 1))
                # print("New pitch: " + str(offsetValue) + " | Chord: ", end=" ")

                # Predict
                probabilities_prediction = self.__model.predict_proba(np.array([chroma]))
                np_prediction = np.array(probabilities_prediction)
                predictions = []

                ids = (-np_prediction).argsort()[:3][0][:3]
                for prediction_id in ids:
                    for chord, value in AUDIO_CONSTANTS.CLASS_MAPPER.items():
                        if value == prediction_id:
                            predictions.append(dict({"Chord": chord,
                                                     "Probability": '{0:.10f}'.format(
                                                         np_prediction[0][prediction_id])}))

                onset_dict = ({"Pitch_start": offsetValue, "Duration": diff, "Predictions": predictions})
                onsets.append(onset_dict)

            print("Sound processing finished.")
            return onsets
