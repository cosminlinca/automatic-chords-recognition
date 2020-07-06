# -*- coding: utf-8 -*-
"""Automatic chord recognition

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CxuCb9kboNEOR6cVH30R52C8VRSKCttQ

## Install librosa
"""

# pip install librosa

"""## Mount Google Drive"""

from google.colab import drive
drive.mount('/content/drive')

"""Check google drive location"""

# !ls "/content/drive/My Drive/Colab Notebooks/IDMT-SMT-CHORDS"

"""# Constants"""

path1 = "/content/drive/My Drive/Colab Notebooks/IDMT-SMT-CHORDS/Split1"
path4 = "/content/drive/My Drive/Colab Notebooks/IDMT-SMT-CHORDS/Split4"
PATH = "/content/drive/My Drive/Colab Notebooks/IDMT-SMT-CHORDS"

"""Parameters"""

fs = 44100          # Sampling frequency = 44.1 KHz
n_bins = 72         # Number of frequency bins
overlap = 0.5       # Hop overlap percentage
cqt_threshold = -61 # Threshold for CQT dB(Decibel) levels, all values before threshold are set to -120 dB
hop_length = 512    # Number of samples between successive frames

"""# Constant-Q Transform - Chromogram


> Load *one song file* and compute chroma vector using Constant-Q Transform

### Imports
"""

# Commented out IPython magic to ensure Python compatibility.
import librosa
import librosa.display
import pickle
# %matplotlib inline
import numpy, scipy, matplotlib.pyplot as plt, IPython.display as ipd

"""### Chord000 - Audio example"""

# 1. Get the file path to the included audio example
song, sr = librosa.load(path4 + "/ableton_live_guitar_Nylon_Concerto_Guitar_001.wav")
ipd.Audio(song, rate=sr)

"""### Create chromagram

- Generate chromagram using chroma_cqt <br>
- Display it using a mathplot
"""

chromagram = librosa.feature.chroma_cqt(song, sr=sr, hop_length=hop_length, n_chroma=12, n_octaves=7)
plt.figure(figsize=(16, 6))
librosa.display.specshow(chromagram, x_axis='time', y_axis='chroma', hop_length=hop_length, cmap='coolwarm')
plt.colorbar()
print(chromagram)
print(chromagram[2].size)

# Write chromagram in file
f = open("chroma.txt", "a")
for x in chromagram:
  for y in x:
    f.write(str(y) + " ")
  f.write("\n")

"""### Chromagram v2"""

plt.figure()
librosa.display.specshow(chromagram, y_axis='chroma', x_axis='time')
plt.title('chroma_cqt')
plt.colorbar()
plt.tight_layout()
plt.show()

"""## Waveplot"""

plt.figure(figsize=(15, 5))
plt.title("Plot - Waveform")
librosa.display.waveplot(song , sr, alpha=0.8)

"""## Melspectrogram"""

mspec = librosa.feature.melspectrogram(y=song, sr=sr, hop_length=hop_length)
librosa.display.specshow(mspec, y_axis='mel', x_axis='time')
mspec.shape

"""## Onset Detection"""

onset_frames = librosa.onset.onset_detect(song, sr=sr)
print(onset_frames) # frame numbers of estimated onsets
print(onset_frames.size)

onset_times = librosa.frames_to_time(onset_frames)
print(onset_times)

"""# TensorFlow & Keras

- Basic classification
> Documentation: https://www.tensorflow.org/tutorials/keras/classification

# T1

## Prepare data

#### Training
"""

## Create chromagrams for input data
import os # for list files from a directory
print(os.listdir(PATH))

split_dir = PATH + "/Split"
train_set = []

for i in range(5, 6):
  # Split directory, index = i
  split_dir = PATH + "/Split"
  split_dir = split_dir + str(i)
  # List songs/chords
  for songFile in os.listdir(split_dir):
    print(songFile)
    songFileAbsolutePath = split_dir + "/" + songFile
    aux = songFile.split("_")
    aux = aux[len(aux)-1]
    if aux.find("wav") > 0:
       aux = int(aux.replace(".wav", ""))
       if(aux <= 38): 
       # Create chromogram
          song, sr  = librosa.load(songFileAbsolutePath)
          chromagram = librosa.feature.chroma_cqt(song, sr=sr, hop_length=hop_length, n_chroma=12, n_octaves=7)
          #train_set.append(chromagram)  
          # Write chromagram in file
          f = open(songFileAbsolutePath.replace(".wav", ".txt"), "w").close()
          f = open(songFileAbsolutePath.replace(".wav", ".txt"), "w")
          for x in chromagram:
            for y in x:
              f.write(str(y) + " ")
            f.write("\n")
    
#print(train_set.shape)

# Create training set
# V2

import os # for list files from a directory
import numpy as np
print(os.listdir(PATH))
split_dir = PATH + "/Split"

train_set = []
for i in range(1, 6):
  # Split directory, index = i
  split_dir = PATH + "/Split"
  split_dir = split_dir + str(i)
  # List songs/chords
  for songFile in os.listdir(split_dir):
    # print(songFile)
    aux = songFile.split("_")
    aux = aux[len(aux)-1]
    if aux.find("txt") > 0:
       aux = int(aux.replace(".txt", ""))
       # print(aux)
       if(aux <= 38): 
          songFileAbsolutePath = split_dir + "/" + songFile.replace(".wav", ".txt")
          # print(songFileAbsolutePath)
          # X_train = np.loadtxt(songFileAbsolutePath, dtype='float')
          # if X_train.size > 0 : 
          #     X_train.reshape(-1, 12, 44)
          #     X_train = np.array(X_train)
              #print(X_train.shape)

          matrix = np.loadtxt(songFileAbsolutePath)
          if matrix.size > 0 :
              X_train = matrix
              train_set.append(X_train)

train_set = np.array(train_set)
print(train_set.shape)

"""**Class names**"""

def ConvertStringToList(string): 
    li = list(string.split("\n")) 
    return li

class_names = ConvertStringToList(open(PATH + "/labels_value.txt").read())
print(len(class_names))

"""#### Testing"""

test_dir = PATH + "/Split1"
print(os.listdir(test_dir))
test_set = []

for songFile in os.listdir(test_dir):
    aux = songFile.split("_")
    aux = aux[len(aux)-1]
    if aux.find("txt") > 0:
       aux = int(aux.replace(".txt", ""))
       if(aux <= 38): 
          songFileAbsolutePath = test_dir + "/" + songFile.replace(".wav", ".txt")
          matrix = np.loadtxt(songFileAbsolutePath)
          if matrix.size > 0 :
              X_test = matrix
              test_set.append(X_test)

test_set = np.array(test_set)
print(test_set.shape)

"""**Labels - Test**"""

def ConvertStringToList(string): 
    li = list(string.split("\n")) 
    return li

test_labels = ConvertStringToList(open(PATH + "/test_labels_value.txt").read())
print(len(test_labels))

"""**Imports**"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.14
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

# (train_chords, train_labels)

"""## Build the model"""

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(12, 44)),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1)
])

# i_sh = train_set[0].shape
# model = Sequential()
# model.add(Dense(16, activation='relu',input_shape=i_sh))
# model.add(Dropout(0.2))
# model.add(Dense(32, activation='relu'))
# model.add(Dropout(0.2))
# model.add(Dense(39, activation='softmax'))

"""## Compile the model"""

model.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics = ['accuracy'])

"""## Train the model"""

#print(train_set)
print(model.summary())
model.fit(np.array(train_set), np.array(class_names), epochs=500)

"""## Evaluate accuracy"""

test_loss, test_acc = model.evaluate(np.array(test_set),  np.array(test_labels), verbose=2)

print('\nTest accuracy:', test_acc)

"""# T2 
# Implementation using guitar_only input

## Imports
"""

import pandas as pd
import tensorflow as tf
import keras
from   keras.layers import Activation, Dense, Dropout, Conv2D, Flatten, MaxPooling2D
from   keras.models import Sequential
import librosa
import librosa.display
import numpy as np

"""## Load chords.csv - labeled data"""

# Labeled data
MAIN_PATH = "/content/drive/My Drive/Colab Notebooks"

data_labeled = pd.read_csv(MAIN_PATH + "/chords.csv")
data_labeled.shape
data_labeled.head(10)

data_labeled['path'] =  data_labeled['classname'].astype('str') + '/' + data_labeled['file_name'].astype('str')
print(data_labeled)

"""## Prepare data"""

train_data = []
print(data_labeled.loc[0].path)
for record in data_labeled.itertuples():
    #print (record)
    song, sr = librosa.load(MAIN_PATH + "/Guitar_Only/" + record.path, duration=2)  
    chromagram = librosa.feature.chroma_cqt(song, sr=sr, hop_length = hop_length, n_chroma=24, n_octaves=7)
    print(chromagram.shape)
    #print(chromagram.shape)
    if chromagram.shape != (12, 44): continue
    train_data.append(chromagram)

print(len(train_data))
print(train_data[0][1])

"""### Using multithreading - #TODO"""

import threading
import time

train_data = []

#Define my thread
class myThread (threading.Thread):
   def __init__(self, threadID, name, start_point, stop):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.start_point = start_point
      self.stop = stop

   def run(self):
      print ("Starting " + self.name + "/n")

      for i in range(start_point, stop):
          song, sr = librosa.load(MAIN_PATH + "/Guitar_Only/" + data_labeled.loc[i].path, duration=2)  
          chromagram = librosa.feature.chroma_cqt(song, sr=sr, hop_length = hop_length, n_chroma=24, n_octaves=7)
          if chromagram.shape != (24, 87): continue
          train_data.append((chromagram, data_labeled.loc[i].classID))

      print ("Exiting /n" + self.name + "/n")

# MAIN
threadLock = threading.Lock()
threads = []

start_point = 0
stop = 199
for i in range(1, 11):
    thread = myThread(i, "Thread " + str(i), start_point, stop)
    thread.start()
    start_point = stop
    stop += 200
    threads.append(thread)
    
  
for i in range(0, 10):
    threads[i].join()

"""## Save training model as numpy file"""

print(len(train_data))
numpy.save(MAIN_PATH + "/data.npy", train_data)

"""## Split DATASET: training + testing"""

#define total dataset
dataset = numpy.load(MAIN_PATH + "/data_chroma24_hop512.npy", allow_pickle=True)
print (len(dataset))

#split
train = dataset[:400]
test = dataset[400:]

print("Training size: " + str(len(train)))
print("Testing size:  " + str(len(test)))

X_train, Y_train = zip(*train)
X_test, Y_test = zip(*test)
print(X_train[0].shape)

# Reshape for CNN input
X_train = np.array([x.reshape( (24, 87, 1) ) for x in X_train])
X_test = np.array([x.reshape( (24, 87, 1) ) for x in X_test])
print(X_train[0].shape)

# One-Hot encoding for classes
Y_train = np.array(keras.utils.to_categorical(Y_train, 10))
Y_test_values = Y_test
Y_test = np.array(keras.utils.to_categorical(Y_test, 10))

print(Y_train[0])

"""## Build the model

How to implement CNN with TensorFlow: 
  - https://www.tensorflow.org/tutorials/images/cnn
  - https://medium.com/@mamarih1/how-to-make-a-cnn-using-tensorflow-and-keras-dd0aaaed8ab4
  - https://towardsdatascience.com/a-comprehensive-guide-to-convolutional-neural-networks-the-eli5-way-3bd2b1164a53
  - YT Tutorial: https://www.youtube.com/watch?v=FmpDIaiMIeA - Realizarea schemei
"""



# Implementation
model = Sequential()
input_shape=(24, 87, 1)

model.add(Conv2D(32, (2, 2), strides=(1, 1), input_shape=input_shape))
model.add(MaxPooling2D())
model.add(Activation('relu'))

model.add(Flatten())
model.add(Dropout(rate=0.5))

model.add(Dense(10))
model.add(Activation('softmax'))

model.summary()

"""## Compile and Run"""

model.compile(
	optimizer="Adam",
	loss="categorical_crossentropy",
	metrics=['accuracy'])

model.fit(
	 x = X_train, 
	 y = Y_train,
    epochs = 10,
    validation_data = (X_test, Y_test))

score = model.evaluate(
	x = X_test,
	y = Y_test)

print('Test accuracy:', score[1])

predictions = model.predict_classes(X_test)
predictions

Y_test_values = np.array(Y_test_values)
Y_test_values