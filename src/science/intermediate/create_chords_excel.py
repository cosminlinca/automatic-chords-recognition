#
# Create an excel based on dataset from DATASET location
# The Excel document will contain:
#  - filename, as complete path
#  - classID, 0...24
#  - classname, a, a#,...n
#

import os

import pandas as pd
from pandas import ExcelWriter
from science.utils import constants as AUDIO_CONSTANTS
chords_dictionary = {'file_name': [], 
                    'classID': [], 
                    'classname': []}

# List subdirectories from dataset directory
# for subDir in os.listdir(DATASET_PATH):
#     currentPath = DATASET_PATH + "//" + subDir
#     if(os.path.isdir(currentPath)):
#         for record in os.listdir(currentPath):
#             chords_dictionary['file_name'].append(record)
#             chords_dictionary['classID'].append(class_mapper[subDir])
#             chords_dictionary['classname'].append(subDir)


# List sub-datasets from dataset directory
for subDataset in os.listdir(AUDIO_CONSTANTS.DATASET_MODIFIED_PATH):
    currentDataset = AUDIO_CONSTANTS.DATASET_MODIFIED_PATH + "//" + subDataset
    if os.path.isdir(currentDataset):
        for subDir in os.listdir(currentDataset):
            currentPath = currentDataset + "//" + subDir
            if os.path.isdir(currentPath):
                for record in os.listdir(currentPath):
                    print(record)
                    chords_dictionary['file_name'].append(currentPath + "//" + record)
                    chords_dictionary['classID'].append(AUDIO_CONSTANTS.CLASS_MAPPER[subDir])
                    chords_dictionary['classname'].append(subDir)


# Create a Pandas dataframe from some data.
df = pd.DataFrame(chords_dictionary)
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = ExcelWriter(AUDIO_CONSTANTS.RESOURCES_PATH + "//" + 'pandas_chords_modified.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')
# Close the Pandas Excel writer and output the Excel file.
writer.save()

