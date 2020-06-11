from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required, fresh_jwt_required, JWTManager, jwt_refresh_token_required,
    jwt_optional, create_access_token, create_refresh_token, get_jwt_identity,
    decode_token
)
from flask_restplus import Resource, Api
from services.UsersService import UsersService
from app import app

users_api = Blueprint('users_api', __name__)

# app = Api(app = app)

users_service = UsersService()

@users_api.route('/users/login',
                 methods = ['POST'])
def login():
    try:
        app.logger.info("in /login")
        json = request.json
        username = json['username']
        password = json['password']
        user_id = users_service.login(username,
                                      password)
        #print(user_id)
        if user_id is None:
            resp = jsonify({'message': 'incorrect username or password'})
            resp.status_code = 401
        else:
            app.logger.info("user_id: " + str(user_id['id']))
            access_token = create_access_token(identity=user_id['id'])
            resp = jsonify({'token': 'Bearer {}'.format(access_token)})
            resp.status_code = 200
        return resp
    except Exception as e:
        print(e)

@users_api.route('/users',
                 methods = ['GET'])
#@jwt_required
def get_users():
    try:
        app.logger.info("in /users")
        user_id = request.args.get('id', default = None, type = int)
        user_name = request.args.get('name', default = None, type = str)
        if user_id is not None:
            user = users_service.get_user_by_id(user_id)
            if user is None:
                resp = jsonify({'message': 'user not found'})
                resp.status_code = 404
            else:
                app.logger.info("user: " + str(user))
                resp = jsonify(user)
                resp.status_code = 200
        elif user_name is not None:
            # Buscar por nombre
            user = users_service.get_user_by_name(user_name)
            if user is None:
                resp = jsonify({'message': 'user not found'})
                resp.status_code = 404
            else:
                app.logger.info("user: " + str(user))
                resp = jsonify(user)
                resp.status_code = 200
        else:
            # Buscar todos los usuarios
            user = users_service.get_all_users()
            app.logger.info("users: " + str(user))
            resp = jsonify(user)
            resp.status_code = 200
        return resp
    except Exception as e:
        print(e)

@users_api.route('/users/userCreate',
                 methods = ['POST'])
def create_new_user():
    try:
        app.logger.info("in /userCreate")
        json = request.json
        email = json['email']
        name = json['name']
        username = json['username']
        password = json['password']
        rowsAffected = users_service.create_new_user(email, name, password, username) #como es insert
        resp = jsonify({'message': 'Succesful'})                                      #se retorna un None
        resp.status_code = 200
    except Exception as e:
        #print(e)
        resp = jsonify({'message': 'Error in registration'})
        resp.status_code = 401
    return resp 

@users_api.route('/ping',
                 methods = ['GET'])
def ping():
    try:
        app.logger.info("in /ping")
        count = users_service.users_count()
        if count > 1:
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


@users_api.route('/users/userId1/<int:id1>/userId2/<int:id2>/send_friend_request',
                 methods = ['GET','POST'])
@jwt_required
def send_friend_request(id1, id2):

    try:
        app.logger.info("in /send-friend-request")
        friend_request = users_service.send_friend_request(id1, id2) #se retorna None si inserto el registro
        if friend_request == False:
            resp = jsonify({'message': 'some id is incorrect, doesnt exist'})
            resp.status_code = 404
        else:
            resp = jsonify({'message': 'Succesful'})                     #False si los ids ingresados no son correctos                 
            resp.status_code = 200
    except Exception as e:
        resp = jsonify({'message': 'Error sending friend request'})
        resp.status_code = 401
    return resp


@users_api.route('/users/<int:user_id>/send_friend_requests',
                 methods = ['GET'])
@jwt_required
def get_friend_request(user_id):
    try:
        app.logger.info("in /send-friend-requests")
        query_friend_request = users_service.get_friend_request(user_id)
        app.logger.info("users: " + str(query_friend_request))
        resp = jsonify(query_friend_request)
        resp.status_code = 200

    except Exception as e:
        resp = jsonify({'message': 'Error in query friend request'})
        resp.status_code = 401
    return resp

@users_api.route('/users/<int:user_id>/friendRequestId/<int:friend_request_id>',
                 methods = ['GET','POST'])
@jwt_required

def accept_reject_friend_request(user_id, friend_request_id):
    try:
        app.logger.info("in /friendRequestId")
        status = request.args.get('status', default = None, type = str)
        #print(status)
        changeStatus = users_service.accept_reject_friend_request(user_id, friend_request_id, status)
        resp = jsonify(changeStatus)
        resp.status_code = 200

    except Exception as e:
        resp = jsonify({'message': 'Error in request'})
        resp.status_code = 401
    return resp