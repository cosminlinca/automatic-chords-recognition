import pandas as pd
from shutil import copyfile
import os

PATH = "F://Licenta//BE.Automatic.Chords.Recognition//dataset"
SPLIT_PATH = "F://Licenta//Split6"
guitar_annotation = pd.read_excel(PATH + "//annotation.xlsx")
# print(guitar_annotation)

# List files from a directory
files = os.listdir(SPLIT_PATH)
# print(files[0])

for i in range(0, 273):
    print(guitar_annotation.loc[i].chord)
    if "E:maj" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "e//" + files[i])
    elif "F:maj" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "f//" + files[i])
    elif "F#:maj" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "f#//" + files[i])
    elif "G:maj" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "g//" + files[i])
    elif "G#:maj" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "g#//" + files[i])
    elif "A:maj" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "a//" + files[i])
    elif "A#:maj" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "a#//" + files[i])
    elif "B:maj" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "b//" + files[i])
    elif "C:maj" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "c//" + files[i])
    elif "C#:maj" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "c#//" + files[i])
    elif "D:maj" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "d//" + files[i])
    elif "D#:maj" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "d#//" + files[i])
    elif "E:min" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "em//" + files[i])
    elif "F:min" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "fm//" + files[i])
    elif "F#:min" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "f#m//" + files[i])
    elif "G:min" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "gm//" + files[i])
    elif "G#:min" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "g#m//" + files[i])
    elif "A:min" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "am//" + files[i])
    elif "A#:min" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "a#m//" + files[i])
    elif "B:min" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "bm//" + files[i])
    elif "C:min" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "cm//" + files[i])
    elif "C#:min" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "c#m//" + files[i])
    elif "D:min" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "dm//" + files[i])
    elif "D#:min" in guitar_annotation.loc[i].chord:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "d#m//" + files[i])
    else:
        copyfile(SPLIT_PATH + "//" + files[i], PATH + "//jams_audio//" + "n//" + files[i])
