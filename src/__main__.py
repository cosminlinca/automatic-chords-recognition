import flask_restful
from flask import Flask

from science.rest.AudioController import AudioController
from science.rest.ConnectionController import ConnectionController

app = Flask(__name__)
api = flask_restful.Api(app)

api.add_resource(AudioController, "/ComputeChordsPrediction")
api.add_resource(ConnectionController, "/Ping")

if __name__ == "__main__":
    app.secret_key = 'CHORDS-RECOGNITION-2020-UBB-LRC'
    print("+ ------------------------------------------------------------------- +")
    print("| Bine ați venit!                                                     |")
    print("|                                                                     |")
    print("| Lucrare de licență: Recunoașterea automată a partiturilor muzicale  |")
    print("| Facultatea de Matematică și Informatică, Informatică Română         |")
    print("| Promoția: 2017-2020                                                 |")
    print("|                                                                     |")
    print("| Autor: Linca Răzvan Cosmin                                          |")
    print("+ ------------------------------------------------------------------- +")
    app.run(debug=True, use_reloader=False, host='0.0.0.0')

