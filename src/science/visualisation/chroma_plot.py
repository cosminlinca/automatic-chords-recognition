import librosa.display
import matplotlib.pyplot as plt
from science.utils import constants as AUDIO_CONSTANTS

# Load a song using librosa loading system
song, sr = librosa.load(AUDIO_CONSTANTS.DATASET_PATH + "//original//am" + "//ableton_live_guitar_Campfire_044.wav")

# Compute chroma
chromagram = librosa.feature.chroma_cqt(song, sr=sr, hop_length=512, n_chroma=24)

plt.figure(figsize=(18, 6))
librosa.display.specshow(chromagram, x_axis='time', y_axis='chroma',
                         hop_length=AUDIO_CONSTANTS.hop_length)
plt.colorbar()
plt.show()
