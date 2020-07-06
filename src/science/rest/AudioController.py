import json
import os

import flask_restful
from flask import request, flash, render_template

from science.model_evaluation.OnsetClassify import OnsetClassify


class AudioController(flask_restful.Resource):
    __UPLOAD_FOLDER = 'F://Licenta//PostAudioUpload//'
    __ALLOWED_EXTENSIONS = {'wav'}

    def __init__(self):
        self.__onsetClassify = None

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.__ALLOWED_EXTENSIONS

    def post(self):
        if 'audio_file' not in request.files:
            flash('No selected file')

        audio_file = request.files['audio_file']
        if audio_file.filename == '':
            flash('No selected file')

        if audio_file and self.allowed_file(audio_file.filename):
            filename = audio_file.filename
            audio_file_path = self.__UPLOAD_FOLDER + filename
            audio_file.save(os.path.join(self.__UPLOAD_FOLDER, filename))
            print("Filename: " + str(audio_file.filename))

            self.__onsetClassify = OnsetClassify(audio_file_path, 0.75)
            onsets = self.__onsetClassify.predict()
            print("Predictions of determined musical intervals were made.")
            print("Results will be returned...Please wait!")

            return json.loads(json.dumps(onsets))
        else:
            return render_template('Invalid file. Please try again!'), 404

            # region POC ChordPrediction
            # chPred = ChordPrediction(audio_file)
            # probabilities_prediction = chPred.predict_proba()
            # np_prediction = np.array(probabilities_prediction)
            #
            # labels_prediction = chPred.predict_classes()
            # print('Labels prediction', labels_prediction)
            #
            # print('Probabilities - numpy prediction', np_prediction)
            # print('Probabilities sum', np_prediction.sum())
            #
            # np.set_printoptions(suppress=True)
            # print('Change printing style - numpy prediction', np_prediction)
            #
            # # Configure json response
            # predictions = []
            # ids = (-np_prediction).argsort()[:3][0][:3]
            # for prediction_id in ids:
            #     for chord, value in AUDIO_CONSTANTS.CLASS_MAPPER.items():
            #         if value == prediction_id:
            #             predictions.append(dict({"Chord": chord,
            #                                      "Probability": '{0:.10f}'.format(np_prediction[0][prediction_id])}))
            #
            # print(predictions)
            # return str(json.dumps(predictions))
            # endregion
