'''
Author: Veerendra Kakumanu
Description: REST API which has enpoints of; List, Create, Get, Update, Delete and Query
'''
from flask import Flask
from flask import request
from pymongo import errors
import json
import re

# Local Imports
from db_connection import Database

QUERY_STRING_PATTERN1 = r'^name=[A-z0-9_]+&data\.[A-z0-9_]+=[A-z0-9_]+$'
QUERY_STRING_PATTERN2 = r'^data\.[A-z0-9_]+=[A-z0-9_]+&name=[A-z0-9_]+$'
QUERY_STRING_PATTERN3 = r'^data\.[A-z0-9_]+=[A-z0-9_]+$'


def validate_json_data(data):  # Make sure the input json satisfy condition
    if "name" not in data or "data" not in data:
        return [False, "The Json should contain 'name' and 'date' keys"]
    elif not re.search(r'^[A-z0-9_]+$', data["name"]):
        return [False, "'name' key string can contains alphanumeric and _"]
    elif not isinstance(data["data"], (list,)):
        return [False, "'data' key's value must has array of json objects"]
    else:
        return [True, "Success", data]


def convert_strings(json_obj, t=None):  # Have to convert all key values int to string. Otherwise mongoDB query fails
    if "name" in json_obj:
        json_obj["name"] = str(json_obj["name"])
    new_data = list()
    if "data" in json_obj:
        for items in json_obj["data"]:
            new_dict = dict((str(k), str(v)) for k, v in items.items())
            new_data.append(new_dict)
    if t == "create":
        return {"name": json_obj["name"], "data": new_data}
    else:
        return {"data": new_data}


def insert_doc(json_content):
    return_list = validate_json_data(json_content)
    if not return_list[0]:
        return json.dumps({"Issue": return_list[1]}), 400
    else:
        db = Database()
        status = db.connect()
        json_content = convert_strings(json_content, "create")
        if not status[0]:
            return json.dumps({"Issue": status[1]}), 500
        try:
            status = db.create_document(json_content)
            if status[0]:
                del(json_content["_id"])
                return json.dumps(json_content)
            else:
                return json.dumps({"Issue": status[1]}), 500
        except errors.ServerSelectionTimeoutError:
            return json.dumps(dict({"Issue": "Failed to Connect DB"}))


def list_docs():
    config_names_list = list()
    db = Database()
    status = db.connect()
    if not status[0]:
        return json.dumps({"Issue": status[1]}), 500
    try:
        status = db.list_documents()
        if status[0]:
            for data in status[2]:
                config_names_list.append(data)
            return json.dumps(dict({"configs": config_names_list}))
        else:
            return json.dumps({"Issue": status[1]}), 500
    except errors.ServerSelectionTimeoutError:
        return json.dumps(dict({"Issue": "Failed to Connect DB"}))


def get_document(doc):
    db = Database()
    status = db.connect()
    if not status[0]:
        return json.dumps({"Issue": status[1]}), 500
    try:
        status = db.get_document(doc)
        if status[0]:
            return str(status[2])
        else:
            return json.dumps({"Issue": status[1]}), 500
    except errors.ServerSelectionTimeoutError:
        return json.dumps(dict({"Issue": "Failed to Connect DB"}))


def delete_doc(doc):
    db = Database()
    status = db.connect()
    if not status[0]:
        return json.dumps({"Issue": status[1]}), 500
    try:
        status = db.purge_document(doc)
        if status[0]:
            return json.dumps({"deleted_count": status[2]})
        else:
            return json.dumps({"Issue": status[1]}), 500
    except errors.ServerSelectionTimeoutError:
        return json.dumps(dict({"Issue": "Failed to Connect DB"}))


def update_doc(config_name, data):
    if "data" not in data or not isinstance(data["data"], list):
        return json.dumps({"Issue": "Invalid data format"})
    db = Database()
    status = db.connect()
    data = convert_strings(data)
    if not status[0]:
        return json.dumps({"Issue": status[1]}), 500
    try:
        status = db.update_document(config_name, data)
        if status[0]:
            return json.dumps({"match_count": status[2].matched_count, "modified_count": status[2].modified_count})
        else:
            return json.dumps({"Issue": status[1]}), 500
    except errors.ServerSelectionTimeoutError:
        return json.dumps(dict({"Issue": "Failed to Connect DB"}))


def query_doc(query_dict):
    config_data = list()
    config_name = None
    db = Database()
    status = db.connect()
    if not status[0]:
        return json.dumps({"Issue": status[1]}), 500
    if len(query_dict) == 1:  # For /search?data.{key}={value}
        key = str(query_dict.keys()[0].replace("data.", ""))
        value = str(query_dict[query_dict.keys()[0]])
        status = db.query(key, value)
    else:  # For /search?name={config_name}&data.{key}={value}
        config_name = str(query_dict["name"])
        del(query_dict["name"])
        key = str(query_dict.keys()[0].replace("data.", ""))
        value = str(query_dict[query_dict.keys()[0]])
        status = db.query(key, value, config_name)
    try:
        if status[0]:
            for data in status[2]:
                del(data["_id"])
                config_data.append(data)
            if config_name is None:
                return json.dumps({"total": len(config_data), "results": config_data})
            else:
                return json.dumps({"total": len(config_data), "results": config_data})
        else:
            return json.dumps({"Issue": status[1]}), 500
    except errors.ServerSelectionTimeoutError:
        return json.dumps(dict({"Issue": "Failed to Connect DB"}))


app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    db = Database()
    status = db.connect()
    return json.dumps({"app": "ok", "db": status[1]})


@app.route('/configs/<config>', methods=['PUT', 'GET', 'DELETE'])
def config_vars(config):
    if request.method == 'GET' and config:
        return get_document(config)
    if request.method == 'DELETE' and config:
        return delete_doc(config)
    if request.method == 'PUT' and config:
        return update_doc(config, request.get_json(force=True))


@app.route('/configs/', methods=['GET', 'POST'])
def config_actions():
    if request.method == 'GET':
        return list_docs()
    if request.method == 'POST':
        return insert_doc(request.get_json(force=True))


@app.route('/search')
def search():
    if request.query_string:
        regex_search1 = re.search(QUERY_STRING_PATTERN1, request.query_string)  # name=test_config&data.last_name=Bluth
        regex_search2 = re.search(QUERY_STRING_PATTERN2, request.query_string)  # data.last_name=Bluth&name=test_config
        regex_search3 = re.search(QUERY_STRING_PATTERN3, request.query_string)  # data.last_name=Bluth
        if regex_search1:
            return query_doc(request.args.to_dict())
        elif regex_search2:
            return query_doc(request.args.to_dict())
        elif regex_search3:
            return query_doc(request.args.to_dict())
        else:
            return json.dumps({"Issue": "Invalid Query String"}), 400
    else:
        return json.dumps({"Issue": "Please Provide Query"}), 400


if __name__ == '__main__':
    app.run()
