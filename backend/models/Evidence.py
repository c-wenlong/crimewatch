from bson.objectid import ObjectId


class Evidence:
    evidence_collection = None  # Initially None

    @classmethod
    def initialize(cls):
        """Lazy initialization of the evidence_collection to avoid circular imports."""
        if cls.evidence_collection is None:
            from mongodb.client import (
                get_evidence_collection,
            )  # Import only when needed

            cls.evidence_collection = get_evidence_collection()
            print("Evidence Collection Initialized: ", cls.evidence_collection)

    def __init__(self, filename, description, extracted_content, file):
        self.filename = filename
        self.description = description
        self.extracted_content = extracted_content
        self.file = file

    def save(self):
        evidence = {
            "filename": self.filename,
            "description": self.description,
            "extracted_content": self.extracted_content,
            "file": self.file,
        }
        self.initialize()
        result = self.evidence_collection.insert_one(evidence)
        return result.inserted_id

    @classmethod
    def find_all(cls):
        cls.initialize()
        try:
            evidences = cls.evidence_collection.find()
            return list(evidences)
        except Exception as e:
            print(e)
            return None

    @classmethod
    def find_by_id(cls, evidence_id):
        cls.initialize()
        try:
            # Add a return statement here to return the found document
            return cls.evidence_collection.find_one({"_id": ObjectId(evidence_id)})
        except Exception as e:
            print(e)
            return None

    @classmethod
    def delete(cls, evidence_id):
        cls.initialize()
        try:
            result = cls.evidence_collection.delete_one({"_id": ObjectId(evidence_id)})
            return result
        except Exception as e:
            print(e)
            return None

    @classmethod
    def update(cls, evidence_id, data):
        cls.initialize()
        try:
            result = cls.evidence_collection.update_one(
                {"_id": ObjectId(evidence_id)}, {"$set": data}
            )
            return result
        except Exception as e:
            print(e)
            return None
