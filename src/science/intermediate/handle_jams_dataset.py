# Example
# import json
#
# JAMS_FILE_PATH = "C://Users//Coss//Downloads//annotation//00_BN1-129-Eb_comp.jams"
#
# with open(JAMS_FILE_PATH) as jamsFile:
#     parsed = json.load(jamsFile)
#
# parsed = json.dumps(parsed)
# converted_json = json.loads(parsed)
# chords = converted_json["annotations"][15]["data"]
# for chord in chords:
#     value = chord["values"]
#     time = chord["time"]
#     duration = chord["duration"]
#

import os
import json
import librosa

JAMS_ANNOTATIONS_PATH = "C://Users//Coss//Downloads//annotation"
JAMS_AUDIO_HEX_PICKUP_DEB_PATH = "C://Users//Coss//Downloads//audio_hex-pickup_debleeded"
JAMS_AUDIO_HEX_PICKUP_ORIGINAL_PATH = "C://Users//Coss//Downloads//audio_hex-pickup_original"
JAMS_AUDIO_MONO_MIC = "C://Users//Coss//Downloads//audio_mono-mic"
JAMS_AUDIO_MONO_PICKUP = "C://Users//Coss//Downloads//audio_mono-pickup_mix"

JAMS_DATASET = "F://Licenta//BE.Automatic.Chords.Recognition//dataset//jams_audio"

jams_annotations_files = os.listdir(JAMS_ANNOTATIONS_PATH)
print(jams_annotations_files)
chordsCounter = 0

for jamFile in jams_annotations_files:
    with open(JAMS_ANNOTATIONS_PATH + "//" + jamFile) as openedJamFile:
        parsed = json.load(openedJamFile)

    # Convert to json as str
    parsed = json.dumps(parsed)
    # Convert string to json
    converted_json = json.loads(parsed)
    chords = converted_json["annotations"][15]["data"]

    # Get corresponding song
    jamName = jamFile.split(".")[0]
    # jamAudioHexPickupDebPath = JAMS_AUDIO_HEX_PICKUP_DEB_PATH + "//" + jamName + "_hex_cln" + ".wav"
    # jamAudioHexPickupOriginalPath = JAMS_AUDIO_HEX_PICKUP_ORIGINAL_PATH + "//" + jamName + "_hex" + ".wav"
    # jamAudioMonoMic = JAMS_AUDIO_MONO_MIC + "//" + jamName + "_mic" + ".wav"
    jamAudioMonoPickup = JAMS_AUDIO_MONO_PICKUP + "//" + jamName + "_mix" + ".wav"

    for chord in chords:
        value = chord["value"]
        # Determine the corresponding category for the chord
        current_chord = "n"
        if value.find("A:maj") != -1:
            current_chord = "a"
        elif value.find("A#:maj") != -1:
            current_chord = "a#"
        elif value.find("A#:min") != -1:
            current_chord = "a#m"
        elif value.find("A:min") != -1:
            current_chord = "am"
        elif value.find("B:maj") != -1:
            current_chord = "b"
        elif value.find("B:min") != -1:
            current_chord = "bm"
        elif value.find("C:maj") != -1:
            current_chord = "c"
        elif value.find("C#:maj") != -1:
            current_chord = "c#"
        elif value.find("C#:min") != -1:
            current_chord = "c#m"
        elif value.find("C:min") != -1:
            current_chord = "cm"
        elif value.find("D:maj") != -1:
            current_chord = "d"
        elif value.find("D#:maj") != -1:
            current_chord = "d#"
        elif value.find("D#:min") != -1:
            current_chord = "d#m"
        elif value.find("D:min") != -1:
            current_chord = "dm"
        elif value.find("E:maj") != -1:
            current_chord = "e"
        elif value.find("E:min") != -1:
            current_chord = "em"
        elif value.find("F:maj") != -1:
            current_chord = "f"
        elif value.find("F#:maj") != -1:
            current_chord = "f#"
        elif value.find("F#:min") != -1:
            current_chord = "f#m"
        elif value.find("F:min") != -1:
            current_chord = "fm"
        elif value.find("G:maj") != -1:
            current_chord = "g"
        elif value.find("G#:maj") != -1:
            current_chord = "g#"
        elif value.find("G#:min") != -1:
            current_chord = "g#m"
        elif value.find("G:min") != -1:
            current_chord = "gm"
        else:
            current_chord = "n"

        time = chord["time"]
        duration = chord["duration"]
        chordsCounter = chordsCounter + 1
        # Spit song using time and duration
        sample_counter = 0
        while duration > 2:
            sample_counter = sample_counter + 1
            aux_duration = 2
            song, sr = librosa.load(jamAudioMonoPickup, duration=aux_duration, offset=time)
            librosa.output.write_wav(JAMS_DATASET + "//" + current_chord + "//" + jamName + "_mix_" +
                                     str(sample_counter) + ".wav", song, sr)

            print(str(aux_duration) + " - " + value + " - " + current_chord)
            duration = duration - aux_duration
            time = time + 2

        sample_counter = sample_counter + 1
        # Process the remaining duration
        if duration > 0.5:
            song, sr = librosa.load(jamAudioMonoPickup, duration=duration, offset=time)
            librosa.output.write_wav(JAMS_DATASET + "//" + current_chord + "//" + jamName + "_mix_" +
                                     str(sample_counter) + ".wav", song, sr)
            print(str(duration) + " - " + value + " - " + current_chord)

print(chordsCounter)


