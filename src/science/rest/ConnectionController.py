import json
import os

import flask_restful
from flask import request, flash, render_template


class ConnectionController(flask_restful.Resource):

    def post(self):
        return "BE is on!"
