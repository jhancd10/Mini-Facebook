from flask import Blueprint
from app import app
from services.PersonsService import PersonsService
from flask import jsonify
from flask import request

persons_api = Blueprint('persons_api', __name__)

persons_service = PersonsService()

@persons_api.route('/persons', methods=['POST'])
def add_person():
    try:
        _json = request.json
        _name = _json["name"]
        _edad = _json["edad"]
        # validate the received values_
        if _name and request.method == 'POST':
            persons_service.add_person(_name, _edad)
            return _name
        else:
            return not_found()
    except Exception as e:
        print(e)

@persons_api.route('/persons', methods=['GET'])
def get_all_persons():
    try:
        app.logger.info("in /persons")      
        rows = persons_service.get_all_persons()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)

@persons_api.route('/persons/<string:name>', methods=['GET'])
def get_person_by_name(name):
    try:
        row = persons_service.get_person_by_name(name)
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@persons_api.route('/persons/relation', methods=['POST'])
def add_new_relationship():
    try:
        _json = request.json
        _name1 = _json["name1"]
        _name2 = _json["name2"]
        # validate the received values
        if _name1 and _name2 and request.method == 'POST':
            persons_service.add_new_relationship(_name1, _name2)
            return _name1, _name2
        else:
            return not_found()
    except Exception as e:
        print(e)


@persons_api.route('/persons/<string:name>/friends', methods=['GET'])
def get_friends(name):
    try:
        row = persons_service.get_friends(name)
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)

@persons_api.route('/persons/<string:name>/maybe-your-know', methods=['GET'])
def get_friends_from_my_friends(name):
    try:
        row = persons_service.get_friends_from_my_friends(name)
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)

@persons_api.route('/persons', methods=['DELETE'])
def delete_new_relationship():
    try:
        _json = request.json
        _name1 = _json["name1"]
        _name2 = _json["name2"]
        # validate the received values
        if _name1 and _name2 and request.method == 'DELETE':
            persons_service.delete_new_relationship(_name1, _name2)
            return _name1, _name2
        else:
            return not_found()
    except Exception as e:
        print(e)


@persons_api.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp