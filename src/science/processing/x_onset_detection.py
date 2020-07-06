#
# Detect chords using LOADED MODEL and classic ONSET DETECTION algorithm
#


from keras.models import load_model
from science.utils.metrics import *
import librosa.display
import numpy as np
from science import utils as AUDIO_CONSTANT

audio_file = "//Let it Be (The Beatles) Strum Guitar Cover with ChordsLyrics.wav"

song, sr = librosa.load(AUDIO_CONSTANT.DATASET_PATH + "//training_songs" + audio_file)
onset_frames = librosa.onset.onset_detect(song, sr=sr, backtrack=True)
# print(onset_frames) # frame numbers of estimated onsets
print(onset_frames.size)

onset_times = librosa.frames_to_time(onset_frames)
print(onset_times)

# Load chroma model
model = load_model(AUDIO_CONSTANT.RESOURCES_PATH + "//model_output" + "//model_V2_2_ChordsRecognition_ConvNet_85.h5",
                   custom_objects={'precision': precision, 'recall': recall, 'f1measure': f1measure})
offsetValue = 0
i = 0

# Minor length for measurable input sample
beta = 0.5
while i < (len(onset_times) - 1):
    offsetValue = onset_times[i]
    diff = onset_times[i + 1] - offsetValue
    while diff < beta and i < (len(onset_times) - 1):
        diff = onset_times[i + 1] - offsetValue
        i = i + 1

    if diff > 2:
        x = diff - 2
        diff = diff - x
        # print ("Diff: " + str(diff))

    song, sr = librosa.load(AUDIO_CONSTANT.DATASET_PATH + "//training_songs" + audio_file,
                            offset=offsetValue, duration=diff)

    chromagram = librosa.feature.chroma_cqt(song, sr=sr, hop_length=AUDIO_CONSTANT.hop_length, n_chroma=24, n_octaves=7)

    aux_chroma = []
    if chromagram.shape < (24, 87):
        for row in chromagram:
            while len(row) < 87:
                row = np.append(row, [0])

            aux_chroma.append(row)
        chromagram = np.array(aux_chroma)

    i = i + 1

    chromagram = chromagram.reshape((24, 87, 1))
    print("New pitch: " + str(offsetValue) + " | Chord: ", end=" ")

    # Predict
    prediction = model.predict_classes(np.array([chromagram]))

    # Find corresponding chord in class_mapper
    for chord, value in AUDIO_CONSTANT.CLASS_MAPPER.items():
        if value == prediction[0]:
            print(chord)
