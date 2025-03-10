from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

try:
    MONGODB_URI = os.getenv("MONGODB_URI")
    print("MONGODB_URI:", MONGODB_URI)
    client = MongoClient(MONGODB_URI)

    # Ping MongoDB to check connection
    client.admin.command("ping")
    print("✅ Successfully connected to MongoDB!")

    DATABASE_NAME = os.getenv("DATABASE_NAME")
    database = client[DATABASE_NAME]

except Exception as e:
    raise Exception(f"🚨 Failed to connect to MongoDB: {e}")


def get_case_collection():
    CASE_COLLECTION = os.getenv("CASE_COLLECTION")
    case_collection = database[CASE_COLLECTION]
    return case_collection


def get_person_collection():
    PERSON_COLLECTION = os.getenv("PERSON_COLLECTION")
    person_collection = database[PERSON_COLLECTION]
    return person_collection


def get_event_collection():
    EVENT_COLLECTION = os.getenv("EVENT_COLLECTION")
    event_collection = database[EVENT_COLLECTION]
    return event_collection

def get_evidence_collection():
    EVIDENCE_COLLECTION = os.getenv("EVIDENCE_COLLECTION")
    evidence_collection = database[EVIDENCE_COLLECTION]
    return evidence_collection