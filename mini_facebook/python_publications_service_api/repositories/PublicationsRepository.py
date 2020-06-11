from pymongo import MongoClient
from app import app
import db_config

class PublicationsRepository(object):
    def __init__(self):
        self.client = MongoClient(app.config['mongodb_url'],
                                  username=app.config['mongodb_username'],
                                  password=app.config['mongodb_password'],
                                  maxPoolSize=10)

    def count(self):
        print("count all publications...")
        db = self.client['publicationsDB']
        return db.publications.count_documents({})

    def create_publication(self, publication):
        db = self.client['publicationsDB'] 
        result = db.publications.insert_one(publication)
        print('One post: {0}'.format(result.inserted_id))
        return True
    
    def publications_by_id(self, idusr):
        db = self.client['publicationsDB']
        return db.publications.find( { 'user_id': int(idusr) }, {'_id': 0} )
