from flask_pymongo import PyMongo
from bson.objectid import ObjectId


class Person:
    person_collection = None  # Initially None

    @classmethod
    def initialize(cls):
        """Lazy initialization of the person_collection to avoid circular imports."""
        if cls.person_collection is None:
            from mongodb.client import get_person_collection  # Import only when needed

            cls.person_collection = get_person_collection()
            print("Person Collection Initialized: ", cls.person_collection)

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
        self.initialize()
        result = self.person_collection.insert_one(person)
        return result.inserted_id

    @classmethod
    def find_all(cls):
        cls.initialize()
        try:
            persons = cls.person_collection.find()
            return list(persons)
        except Exception as e:
            print(e)
            return None

    @classmethod
    def find_by_id(cls, person_id):
        cls.initialize()
        try:
            # Add a return statement here to return the found document
            return cls.person_collection.find_one({"_id": ObjectId(person_id)})
        except Exception as e:
            print(e)
            return None

    @classmethod
    def delete(cls, person_id):
        cls.initialize()
        try:
            result = cls.person_collection.delete_one({"_id": ObjectId(person_id)})
            return result
        except Exception as e:
            print(e)
            return None

    @classmethod
    def update(cls, person_id, data):
        cls.initialize()
        try:
            result = cls.person_collection.update_one(
                {"_id": ObjectId(person_id)}, {"$set": data}
            )
            return result
        except Exception as e:
            print(e)
            return None
