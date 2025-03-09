from flask_pymongo import PyMongo
from bson.objectid import ObjectId

mongo = PyMongo()

class Event:
    def __init__(self, case_id, person_id, event_type, description, location, reported_by, occurred_at, reported_at):
        self.case_id = case_id
        self.person_id = person_id
        self.event_type = event_type
        self.description = description
        self.location = location
        self.reported_by = reported_by
        self.occurred_at = occurred_at
        self.reported_at = reported_at

    def save(self):
        event = {
            "case_id": self.case_id,
            "person_id": self.person_id,
            "event_type": self.event_type,
            "description": self.description,
            "location": self.location,
            "reported_by": self.reported_by,
            "occurred_at": self.occurred_at,
            "reported_at": self.reported_at
        }
        result = mongo.db.events.insert_one(event)
        return result.inserted_id

    @classmethod
    def find_by_id(cls, event_id):
        event = mongo.db.events.find_one({"_id": ObjectId(event_id)})
        return event

    @classmethod
    def delete(cls, event_id):
        result = mongo.db.events.delete_one({"_id": ObjectId(event_id)})
        return result
