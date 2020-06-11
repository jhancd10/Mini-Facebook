from repositories.PersonsRepository import PersonsRepository

class PersonsService(object):
    def __init__(self):
        self.persons_repository = PersonsRepository()

    def add_person(self, name, edad):
         return self.persons_repository.add_person(name, edad)

    def get_all_persons(self):
        return self.persons_repository.get_all_persons()

    def get_person_by_name(self, name):
        return self.persons_repository.get_person_by_name(name)

    def add_new_relationship(self, name1, name2):
        return self.persons_repository.add_new_relationship(name1, name2)
    
    def delete_new_relationship(self, personId1, personId2):
        return self.persons_repository.delete_new_relationship(personId1, personId2)

    def get_friends(self, name):
        return self.persons_repository.get_friends(name)

    def get_friends_from_my_friends(self, name):
        return self.persons_repository.get_friends_from_my_friends(name)