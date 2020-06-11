from flask import Blueprint
import db_config
from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required, fresh_jwt_required, JWTManager, jwt_refresh_token_required,
    jwt_optional, create_access_token, create_refresh_token, get_jwt_identity,
    decode_token
)
from services.PublicationsService import PublicationsService
from app import app

publications_api = Blueprint('publications_api', __name__)

publications_service = PublicationsService()

@publications_api.route('/publications', methods = ['POST'])
#@jwt_required
def create_publication():
    try:
        app.logger.info("in /publications")
        publication_body = request.json
        if 'user_id' in publication_body and 'description' in publication_body:
            app.logger.info("user_id: " + str(publication_body['user_id']) + ' - description: ' + str(publication_body['description']))
            result = publications_service.send_publication(publication_body)
            if result:
                resp = jsonify({'message': 'publication received'})
                resp.status_code = 201
            else:
                resp = jsonify({'message': 'publication was not received'})
                resp.status_code = 500
        else:
            resp = jsonify({'message': 'the server was unable to process the request sent by the client due to invalid message syntax'})
            resp.status_code = 400
        return resp
    except Exception as e:
        resp = jsonify({'message': 'unknown error'})
        resp.status_code = 500
        return resp

@publications_api.route('/publication/user/', methods = ['POST'])
#@jwt_required
def new_publication():
    try:
        app.logger.info("in /publication")
        publication_body = request.json
        if 'user_id' in publication_body and 'description' in publication_body:
            app.logger.info("user_id: " + str(publication_body['user_id']) + ' - description: ' + 
            str(publication_body['description']))
            result = publications_service.insert_publication(publication_body)
            if result:
                resp = jsonify({'message': 'publication inserted'})
                resp.status_code = 201
            else:
                resp = jsonify({'message': 'publication was not inserted'})
                resp.status_code = 500
        else:
            resp = jsonify({'message': 'the server was unable to process the request sent by the client due to invalid message syntax'})
            resp.status_code = 400
        return resp
    except Exception as e:
        resp = jsonify({'message': 'unknown error'})
        resp.status_code = 500
        return resp

@publications_api.route('/publication/user/<string:user_id>', methods=['GET'])
#@jwt_required
def get_publications(user_id):
    try:
        if user_id != "":
            result = publications_service.get_all_publication(user_id)
            if (len(result) > 0):
                resp = jsonify(result)
                resp.status_code = 201
            else:
                resp = jsonify({'message': 'There are not publications to show.'})
                resp.status_code = 500
        else:
            resp = jsonify({'message': 'the server was unable to process the request sent by the client due to invalid message syntax'})
            resp.status_code = 400
        return resp

    except Exception as e:
        resp = jsonify({'message': 'unknown error'})
        resp.status_code = 500
        return resp

@publications_api.route('/publication/user/<string:user_id>/friends=<string:wildcard>', methods=['GET'])
#@jwt_required
def get_friends_publications(user_id, wildcard):
    try:
        if user_id != "":
            if wildcard == 'true':
                return get_publications(user_id)
            else:
                resp = jsonify({'message': 'They are not friends.'})
                resp.status_code = 500
        else:
            resp = jsonify({'message': 'the server was unable to process the request sent by the client due to invalid message syntax'})
            resp.status_code = 400
        return resp
    except Exception as e:
        resp = jsonify({'message': 'unknown error'})
        resp.status_code = 500
        return resp

@publications_api.route('/publications/ping', methods = ['GET'])
def ping():
    try:
        app.logger.info("in /ping")
        count = publications_service.documents_count()
        if count >= 0:
            resp = jsonify({'message': 'pong'})
            resp.status_code = 200
        else:
            resp = jsonify({'message': 'error'})
            resp.status_code = 500
    except Exception as e:
        app.logger.error(str(e))
        resp = jsonify({'message': 'error'})
        resp.status_code = 500
    return resp