# import datetime
# import logging
# import os
#
# import keras
# from keras.layers import Activation, Dense, Dropout, Conv2D, MaxPooling2D, BatchNormalization, \
#     GlobalAveragePooling2D
# from keras.models import Sequential
#
# import utils.constants as AUDIO_CONSTANTS
# from utils.logging import logging_setup
# from utils.metrics import *
#
# # Custom logging
# logging_setup()
# # Use logging system
# logger = logging.getLogger('src.modelling.ChRecogCNN')
#
#
# class ChRecogCNN:
#
#     def __init__(self, name, input_shape):
#         self.input_shape = input_shape
#         self.name = name
#         self.score_train = []
#         self.score_test = []
#
#         logger.info("Initializing CNN")
#         logger.info(f"Input shape = {self.input_shape}")
#         self.model = Sequential()
#
#         self.model.add(Conv2D(32, (3, 3), input_shape=input_shape))
#         self.model.add(BatchNormalization())
#         self.model.add(Activation('relu'))
#         self.model.add(Dropout(rate=0.25))
#
#         self.model.add(Conv2D(32, (3, 3), input_shape=input_shape))
#         self.model.add(BatchNormalization())
#         self.model.add(Activation('relu'))
#         self.model.add(Dropout(rate=0.25))
#
#         self.model.add(Conv2D(32, (3, 3), input_shape=input_shape))
#         self.model.add(BatchNormalization())
#         self.model.add(Activation('relu'))
#         self.model.add(Dropout(rate=0.5))
#
#         self.model.add(MaxPooling2D())
#
#         self.model.add(Conv2D(64, (3, 3), input_shape=input_shape))
#         self.model.add(BatchNormalization())
#         self.model.add(Activation('relu'))
#         self.model.add(Dropout(rate=0.25))
#
#         self.model.add(Conv2D(64, (3, 3), input_shape=input_shape))
#         self.model.add(BatchNormalization())
#         self.model.add(Activation('relu'))
#         self.model.add(Dropout(rate=0.25))
#
#         # self.model.add(MaxPooling2D())
#
#         # self.model.add(Conv2D(25, (1, 1), input_shape=input_shape))
#         # self.model.add(BatchNormalization())
#         # self.model.add(Activation('relu'))
#         # self.model.add(Dropout(rate=0.25))
#
#         self.model.add(Dense(128))
#         self.model.add(Activation('relu'))
#         self.model.add(Dropout(rate=0.25))
#
#         self.model.add(GlobalAveragePooling2D())
#
#         self.model.add(Dense(25))
#         self.model.add(Activation('softmax'))
#         logger.info("CNN Initialized")
#
#     def __str__(self):
#         return str(self.model.summary())
#
#     def train(self, X_train, Y_train, X_test, Y_test):
#         logger.info("Start training model")
#
#         self.model.compile(
#             optimizer="Adam",
#             loss="categorical_crossentropy",
#             metrics=['accuracy', precision, recall, f1measure])
#
#         # TensorBoard Logging
#         log_dir = os.path.join(AUDIO_CONSTANTS.LOGGING_PATH, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
#         tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
#
#         logger.info("Tensorboard Logging Started")
#         logger.info("Use the following command in the terminal to view the logs during training: tensorboard
#         --logdir "
#                     "logs/training")
#
#         self.model.fit(
#             x=X_train,
#             y=Y_train,
#             epochs=10,
#             batch_size=128,
#             validation_data=(X_test, Y_test),
#             callbacks=[tensorboard_callback])
#
#         logger.info("Training completed")
#
#     def evaluate(self, X_train, Y_train, X_test, Y_test):
#         self.score_train = self.model.evaluate(
#             x=X_train,
#             y=Y_train)
#
#         self.score_test = self.model.evaluate(
#             x=X_test,
#             y=Y_test)
#
#         logger.info(f'Train loss: {self.score_train[0]}')
#         logger.info(f'Train accuracy: {self.score_train[1]}')
#         logger.info(f'Train precision: {self.score_train[2]}')
#         logger.info(f'Train recall: {self.score_train[3]}')
#         logger.info(f'Train f1-score: {self.score_train[4]}')
#
#         logger.info(f'Test loss: {self.score_test[0]}')
#         logger.info(f'Test accuracy: {self.score_test[1]}')
#         logger.info(f'Test precision: {self.score_test[2]}')
#         logger.info(f'Test recall: {self.score_test[3]}')
#         logger.info(f'Test f1-score: {self.score_test[4]}')
#
#     def save_model(self):
#         logger.info("Saving model")
#         model_path = AUDIO_CONSTANTS.RESOURCES_PATH + "//" + self.name + ".h5"
#         self.model.save(model_path)
#         logger.info("Model saved to " + model_path)
