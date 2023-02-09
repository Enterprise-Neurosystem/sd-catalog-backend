#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 18:27:36 2022

@author: dineshverma
@author: aninditadas
"""

from flask import Blueprint, current_app, request, jsonify
from dataclasses import dataclass, asdict
import json

from catalog.errors import MissingIdentity, MissingJSON, ItemNotFound, MissingInputException
from catalog.sda_db import MongoDBase, SelfDescribingEntry, SelfDescribingEntryConverter

sda_blueprint = Blueprint('sda_blueprint', __name__, url_prefix='/sda')
DB_TAG = "DB_TAG"
ID_TERM = "_id"
QUERY_FIELD = "search"


def _initialize_sda_views(app):
    app.register_blueprint(sda_blueprint)
    db_url = app.config["MONGO_URL"]
    db_name = app.config["SDA_DB_NAME"]
    db_coll = app.config["SDA_COLL_NAME"]
    app.config[DB_TAG] = MongoDBase(SelfDescribingEntryConverter(), db_url, db_name, db_coll)


def get_db():
    answer = current_app.config.get(DB_TAG, None)
    if answer is None:
        db_url = current_app.config["MONGO_URL"]
        db_name = current_app.config["SDA_DB_NAME"]
        db_coll = current_app.config["SDA_COLL_NAME"]
        current_app.config[DB_TAG] = MongoDBase(SelfDescribingEntryConverter(), db_url, db_name, db_coll)
        answer = current_app.config[DB_TAG]
    return answer


@dataclass
class MyResponse:
    _id: str
    code: int

    def to_json(self):
        return json.dumps(asdict(self))


@dataclass
class MyResponseWithEntry(MyResponse):
    item: SelfDescribingEntry = None


def make_entry_response(identity, code, item=None):
    response = None
    if item is None:
        response = MyResponse(identity, code)
    else:
        response = MyResponseWithEntry(identity, code, item)
    return response.to_json()


def get_request_id(request_type):
    entry = get_request_json()
    this_id = entry.get(ID_TERM, None)
    if this_id is None:
        raise MissingIdentity(request_type)
    return this_id


def get_request_json():
    entry = request.get_json()
    if entry is None:
        raise MissingJSON()
    return entry


def get_request_field(entry, field):
    answer = entry.get(field, None)
    if answer is None:
        raise MissingInputException(field, entry)
    return answer


@sda_blueprint.route("/create", methods=['POST'])
def create_request():
    db = get_db()
    entry = request.get_json()
    if entry is None:
        raise MissingJSON()
    item = SelfDescribingEntry.from_dict(entry)
    identity = db.create(item)
    item.set_identity(identity)
    return item.to_json()


@sda_blueprint.route("/retrieve/<string:asset_id>", methods=['GET'])
def retrieve_request(asset_id):
    db = get_db()
    result = db.retrieve(asset_id)
    if result is None:
        raise ItemNotFound(asset_id)
    return jsonify(result)


@sda_blueprint.route("/delete/<string:asset_id>", methods=['GET'])
def delete_request(asset_id):
    db = get_db()
    num_records_deleted = db.delete(asset_id)
    if num_records_deleted == 0:
        raise ItemNotFound(asset_id)
    else:
        resp = jsonify('Asset deleted successfully!')
        resp.status_code = 200
        return resp


@sda_blueprint.route("/update", methods=['POST'])
def update_request():
    db = get_db()
    this_id = get_request_id("update")
    item = db.retrieve(this_id)
    if item is not None:
        json_entry = request.get_json()
        if json_entry is None:
            raise MissingJSON()
        json_entry.pop(ID_TERM, None)
        db.update(this_id, json_entry)
        item = db.retrieve(this_id)
    if item is None:
        raise ItemNotFound(this_id)
    return item.to_json()


@sda_blueprint.route("/list", methods=['GET'])
def list_request():
    db = get_db()
    elements = db.get_all()
    return jsonify(elements)


@sda_blueprint.route("/search", methods=['POST'])
def search_request():
    db = get_db()
    query = get_request_field(QUERY_FIELD, get_request_json())
    elements = db.search(query)
    answer = "{"
    for elem in elements:
        answer = answer + elem.to_json()
    answer = answer + "}"
    return answer


@sda_blueprint.route("/purge", methods=['POST'])
def purge_request():
    db = get_db()
    db.purge()

    return ""
