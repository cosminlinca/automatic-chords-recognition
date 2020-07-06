#
# KERAS Training + Testing
# TODO - Refactoring
#


# -------------------------------------------------------------------------------------------------------------------

# Define total dataset
# Split in training/testing
# Load dataset from .npy file
# dataset = np.load(RESOURCES_PATH + "//data_chroma24_hop512_V2.npy", allow_pickle=True)
# random.shuffle(dataset)

# train = dataset[:13500]
# test = dataset[13500:]

# print("Training size: " + str(len(train)))
# print("Testing size:  " + str(len(test)))

# X_train, Y_train = zip(*train)
# X_test, Y_test = zip(*test)
# print(X_train[0].shape)

# # Reshape for CNN input
# X_train = np.array([x.reshape( (24, 87, 1) ) for x in X_train])
# X_test = np.array([x.reshape( (24, 87, 1) ) for x in X_test])
# print(X_train[0].shape)

# # One-Hot encoding for classes
# Y_train = np.array(keras.utils.to_categorical(Y_train, 25))
# Y_test_values = Y_test
# Y_test = np.array(keras.utils.to_categorical(Y_test, 25))

# print(Y_train[0])


# # Implementation
# model = Sequential()
# input_shape=(24, 87, 1)

# model.add(Conv2D(24, (2, 2), input_shape=input_shape))
# model.add(MaxPooling2D())
# model.add(Activation('relu'))

# model.add(Conv2D(32, (2, 2), padding="valid"))
# model.add(Activation('relu'))

# model.add(Flatten())
# model.add(Dropout(rate=0.5))

# model.add(Dense(128))
# model.add(Activation('relu'))
# model.add(Dropout(rate=0.5))

# model.add(Dense(25))
# model.add(Activation('softmax'))

# model.summary()

# model.compile(
# 	optimizer="Adam",
# 	loss="categorical_crossentropy",
# 	metrics=['accuracy'])

# model.fit(
# 	 x = X_train, 
# 	 y = Y_train,
#     epochs = 25,
#     validation_data = (X_test, Y_test))

# score = model.evaluate(
# 	x = X_test,
# 	y = Y_test)

# print('Test accuracy:', score[1])

# predictions = model.predict_classes(X_test)
# predictions

# Y_test_values=np.array(Y_test_values)
# Y_test_values


# model.save(RESOURCES_PATH + "//model_alfa_chroma24_hop512.h5")
# print ("Model evaluation is done...Please check the results!")


### TEST
# -------------------------------------------------------------------------------------------------------

# # Test saved model using custom input => predict_classes
# from keras.models import load_model
# import utils.audio_constants as AUDIO_CONSTANTS
#
# model = load_model(AUDIO_CONSTANTS.RESOURCES_PATH + "//model_output" + "//model_alfa_chroma24_hop512.h5")
# input_for_prediction = "F://Licenta//Other_Instruments//Accordion//dm//dm1.wav"
#
# song, sr = librosa.load(input_for_prediction, duration=2)
# chromagram = librosa.feature.chroma_cqt(song, sr=sr, hop_length = AUDIO_CONSTANTS.hop_length, n_chroma=24,
#                                           n_octaves=7)
# aux_chroma = []
# if chromagram.shape != (24, 87):
#     for row in chromagram:
#         while len(row) < 87:
#             row = np.append(row, [0])
#
#         aux_chroma.append(row)
#     chromagram = np.array(aux_chroma)
#
#
# chromagram = chromagram.reshape((24, 87, 1))
# print(model.predict_classes(np.array([chromagram])))
