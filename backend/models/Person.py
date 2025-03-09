from flask_pymongo import PyMongo
from bson.objectid import ObjectId

mongo = PyMongo()


class Person:
    def __init__(self, name, age, gender, known_addresses, role_in_case):
        self.name = name
        self.age = age
        self.gender = gender
        self.known_addresses = known_addresses
        self.role_in_case = role_in_case

    def save(self):
        person = {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "known_addresses": self.known_addresses,
            "role_in_case": self.role_in_case,
        }
        result = mongo.db.people.insert_one(person)
        return result.inserted_id

    @classmethod
    def find_by_id(cls, person_id):
        person = mongo.db.people.find_one({"_id": ObjectId(person_id)})
        return person

    @classmethod
    def delete(cls, person_id):
        result = mongo.db.people.delete_one({"_id": ObjectId(person_id)})
        return result
