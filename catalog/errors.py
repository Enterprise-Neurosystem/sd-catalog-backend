#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 16:15:10 2022

@author: dineshverma
"""
from flask import Blueprint, jsonify, render_template
import os
import traceback

errors = Blueprint('errors', __name__)


class CatalogException(Exception):
    def __init__(self, message):
        self.message = message
        self.code = 500


class MissingArgumentException(CatalogException):
    def __init__(self, arg_name, class_name):
        super().__init__(f"Argument {arg_name} required for creating {class_name}")


class MissingIdentity(CatalogException):
    def __init__(self, request_type):
        super().__init__(f"Identity field is required for {request_type} request")


class InvalidArgumentException(CatalogException):
    def __init__(self, passed_value, field_name, entry_name):
        super().__init__(f"The value {passed_value} is not allowed for {field_name} in {entry_name}")


class ItemNotFound(CatalogException):
    def __init__(self, identity):
        super().__init__(f"No items with id of {identity} found")


class MissingJSON(CatalogException):
    def __init__(self):
        super().__init__("No JSON field specified in the request")


class DuplicateEntryException(CatalogException):
    def __init__(self, entry_name, field_name, value_name):
        super().__init__(f"An {entry_name} with {field_name} of {value_name} already exists")


class MissingInputException(CatalogException):
    def __init__(self, arg_name, entry):
        super().__init__(f"Field {arg_name} missing in request input {entry}")


class WebException(Exception):
    def __init__(self, catalog_exception=None, message=None, code=500):
        if catalog_exception is not None:
            self.message = catalog_exception.message
            self.code = catalog_exception.code
            self.underlying_excption = catalog_exception
        else:
            self.message = message
            self.code = code
            self.underlying_excption = None


def _initialize_errorhandlers(application):
    '''
    Initialize error handlers
    '''
    application.register_blueprint(errors)
    # g.error_message = " "


@errors.app_errorhandler(CatalogException)
def handle_error(error):
    message = error.message
    status_code = error.code
    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }

    return jsonify(response), status_code


# @errors.context_processor
# def message_processor():
# return dict(message=g.error_message)

@errors.app_errorhandler(WebException)
def show_error_page(error):
    # g.error_message = get_display_error_message(error)
    return render_template("error.html", messages=get_display_error_message(error))


def get_display_error_message(error):
    orig = 'An unexpected error has occurred.'
    debug_mode = os.getenv('FLASK_ENV')

    if isinstance(error, WebException):
        if error.underlying_excption is not None:
            error = error.underlying_excption

    if isinstance(error, (CatalogException, WebException)):
        orig = error.message

    if debug_mode == "development":
        messages = [orig]
        if not isinstance(error, (CatalogException, WebException)):
            messages = messages + [str(x) for x in error.args]
        messages = messages + traceback.format_exc().split('\n')
        return messages
    return [orig]


@errors.app_errorhandler(Exception)
def handle_unexpected_error(error):
    status_code = 500
    message = get_display_error_message(error)

    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }

    return jsonify(response), status_code
