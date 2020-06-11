from neo4j import GraphDatabase
from db_config import driver

class PersonsRepository(object):

    def add_person(self, name, edad):
        with driver.session() as session:
            result = session.run("CREATE (n:Person{name:$_name, edad:$_edad})",
                                 _name=name, _edad=edad).value()
            return result

    def get_all_persons(self):
        with driver.session() as session:
            result = session.run("MATCH (n:Person) RETURN n.name as name LIMIT 25").data()
            return result

    def get_person_by_name(self, name):
        with driver.session() as session:
            result = session.run("MATCH (n:Person {name: $name}) RETURN n.name as name, n.age as age", name=name).data()
            return result

    def add_new_relationship(self, name1, name2):
        with driver.session() as session:
            result = session.run("Match (p1:Person{name:$name1})"
                   "Match (p2:Person{name:$name2})"
                   "Create (p1)-[:FRIEND]->(p2)",name1=name1, name2=name2).value()
            return result
    
    def delete_new_relationship(self, name1, name2):
        with driver.session() as session:
            result = session.run("Match (p1:Person{name:$name1}) -[r:FRIEND]->(p2:Person{name:$name2})"
                   "DELETE r",name1=name1, name2=name2).value()
            return result

    def get_friends(self, name):
        with driver.session() as session:
            result = session.run("MATCH ( n {name: $name})-[:FRIEND]->(fof) RETURN fof.edad as age, fof.name as name",name=name).data()
            return result

    def get_friends_from_my_friends(self, name):
        with driver.session() as session:
            result = session.run("MATCH (n {name: $name})-[:FRIEND]->()-[:FRIEND]->(fof) RETURN fof.edad as age, fof.name as name",name=name).data()
            return result   