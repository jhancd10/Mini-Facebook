from repositories.UsersRepository import UsersRepository
from app import app


class UsersService(object):
    def __init__(self):
        self.users_repository = UsersRepository()

    def login(self,
              username,
              password):
        return self.users_repository.login(username,
                                           password)

    def get_user_by_id(self, id):
        return self.users_repository.get_user_by_id(id)

    def get_user_by_name(self, name):
        return self.users_repository.get_user_by_name(name)
    
    def get_all_users(self):
        return self.users_repository.get_all_users()
    
    def create_new_user(self, email, name, password, username):
        return self.users_repository.create_new_user(email, name, password, username)

    def users_count(self):
        response = self.users_repository.count()
        return int(response['count'])

    def send_friend_request(self, id1, id2):
        return self.users_repository.send_friend_request(id1, id2)

    def get_friend_request(self, id):
        return self.users_repository.get_friend_request(id)

    def accept_reject_friend_request(self, id1, id2, status):
        return self.users_repository.accept_reject_friend_request(id1,id2, status)