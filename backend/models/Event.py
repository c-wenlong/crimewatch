from flask_pymongo import PyMongo
from bson.objectid import ObjectId


class Event:
    event_collection = None  # Initially None

    @classmethod
    def initialize(cls):
        """Lazy initialization of the event_collection to avoid circular imports."""
        if cls.event_collection is None:
            from mongodb.client import get_event_collection  # Import only when needed

            cls.event_collection = get_event_collection()
            print("Event Collection Initialized: ", cls.event_collection)

    def __init__(
        self,
        case_id,
        person_id,
        event_type,
        description,
        location,
        reported_by,
        occurred_at,
        reported_at,
    ):
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
            "reported_at": self.reported_at,
        }
        self.initialize()
        result = self.event_collection.insert_one(event)
        return result.inserted_id

    @classmethod
    def find_all(cls):
        cls.initialize()
        try:
            events = cls.event_collection.find()
            return list(events)
        except Exception as e:
            print(e)
            return None

    @classmethod
    def find_by_id(cls, event_id):
        cls.initialize()
        try:
            # Add a return statement here to return the found document
            return cls.event_collection.find_one({"_id": ObjectId(event_id)})
        except Exception as e:
            print(e)
            return None

    @classmethod
    def delete(cls, event_id):
        cls.initialize()
        try:
            result = cls.event_collection.delete_one({"_id": ObjectId(event_id)})
            return result
        except Exception as e:
            print(e)
            return None

    @classmethod
    def update(cls, event_id, data):
        cls.initialize()
        try:
            result = cls.event_collection.update_one(
                {"_id": ObjectId(event_id)}, {"$set": data}
            )
            return result
        except Exception as e:
            print(e)
            return None
