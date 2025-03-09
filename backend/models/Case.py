from flask_pymongo import PyMongo
from bson.objectid import ObjectId

mongo = PyMongo()

class Case:
    def __init__(self, title, description, type_of_crime, reported_location, reported_datetime, investigator_id, people_involved, evidence, event_ids):
        self.title = title
        self.description = description
        self.type_of_crime = type_of_crime
        self.reported_location = reported_location
        self.reported_datetime = reported_datetime
        self.investigator_id = investigator_id
        self.people_involved = people_involved
        self.evidence = evidence
        self.event_ids = event_ids

    def save(self):
        case = {
            "title": self.title,
            "description": self.description,
            "type_of_crime": self.type_of_crime,
            "reported_location": self.reported_location,
            "reported_datetime": self.reported_datetime,
            "investigator_id": self.investigator_id,
            "people_involved": self.people_involved,
            "evidence": self.evidence,
            "event_ids": self.event_ids
        }
        result = mongo.db.cases.insert_one(case)
        return result.inserted_id

    @classmethod
    def find_by_id(cls, case_id):
        case = mongo.db.cases.find_one({"_id": ObjectId(case_id)})
        return case

    @classmethod
    def delete(cls, case_id):
        result = mongo.db.cases.delete_one({"_id": ObjectId(case_id)})
        return result
 