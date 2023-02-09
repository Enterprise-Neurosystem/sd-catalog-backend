#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 14:32:51 2022

@author: dineshverma
"""

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
import os

# from views import self_describing_bp
# from models import SelfDescribingEntryDbase
from catalog.errors import _initialize_errorhandlers
from catalog.sda_view import _initialize_sda_views
from catalog.user_view import _initialize_user_views


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        # load the test configuration from instance path
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Make Sure that instance_path exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # from catalog.views import sda_blueprint
    # app.register_blueprint(sda_blueprint)

    # Swagger config
    SWAGGER_URL = '/apispec'
    API_URL = '/static/apispec.json'
    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "SDA API",
            'defaultModelsExpandDepth': -1,
            'defaultModelRendering': "model",
            'defaultModelExpandDepth': 2
        }
    )
    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

    _initialize_errorhandlers(app)
    _initialize_sda_views(app)
    _initialize_user_views(app)

    # Test configuration
    @app.route('/hello', methods=['GET', 'POST'])
    def hello():
        answer = "<p> " + app.instance_path + " <p>"
        for this_key in app.config.keys():
            answer = answer + "<p> " + this_key + ":" + str(app.config[this_key]) + "</p>"

        return answer

    @app.route('/shello', methods=['GET', 'POST'])
    def shello():
        answer = "<p> " + "Simple Hello " + "<p>"
        return answer

    return app
