CLASS_MAPPER = {'a': 0,
                'a#': 1,
                'a#m': 2,
                'am': 3,
                'b': 4,
                'bm': 5,
                'c': 6,
                'c#': 7,
                'c#m': 8,
                'cm': 9,
                'd': 10,
                'd#': 11,
                'd#m': 12,
                'dm': 13,
                'e': 14,
                'em': 15,
                'f': 16,
                'f#': 17,
                'f#m': 18,
                'fm': 19,
                'g': 20,
                'g#': 21,
                'g#m': 22,
                'gm': 23,
                'n': 24}

RESOURCES_PATH = "F://Licenta//BE.Automatic.Chords.Recognition//resources"
DATASET_PATH = "F://Licenta//BE.Automatic.Chords.Recognition//dataset"
DATASET_MODIFIED_PATH = "F://Licenta//BE.Automatic.Chords.Recognition//dataset_modified"
JAMS_DATASET = "F://Licenta//BE.Automatic.Chords.Recognition//dataset//jams_audio"
JAMS_AUGMENTED_DATASET = "F://Licenta//BE.Automatic.Chords.Recognition//dataset//jams_audio_augmented"
AUXILIARY_DATASET = "F://Licenta//BE.Automatic.Chords.Recognition//dataset//auxiliary_dataset"
AUXILIARY_DATASET_AUGMENTED = "F://Licenta//BE.Automatic.Chords.Recognition//dataset//auxiliary_dataset_augmented"
LOGGING_PATH = "F://Licenta//BE.Automatic.Chords.Recognition//src//science//modelling//logs"
LOGGING_FILE_PATH = "F://Licenta//BE.Automatic.Chords.Recognition//src//logging.yml"

fs = 44100  # Sampling frequency = 44.1 KHz
n_bins = 72  # Number of frequency bins
overlap = 0.5  # Hop overlap percentage
cqt_threshold = -61  # Threshold for CQT dB(Decibel) levels, all values before threshold are set to -120 dB
hop_length = 512  # Number of samples between successive frames
