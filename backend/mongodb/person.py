from flask import Blueprint, request, jsonify
from models import Person
import json
from bson import json_util

# Create a Blueprint for Person Routes
person_routes = Blueprint("person_routes", __name__)


# Create Person
@person_routes.route("/", methods=["POST"])
def create_person():
    data = request.json
    person = Person(**data)
    person_id = person.save()
    return jsonify({"person_id": str(person_id)}), 201


# Test Person Route
@person_routes.route("/test", methods=["GET"])
def test_person():
    return "this is a test for the person route"


# Get all Persons
@person_routes.route("/all", methods=["GET"])
def get_all_persons():
    persons = Person.find_all()
    if persons is None:
        return jsonify({"error": "Person not found"}), 404

    # Convert MongoDB objects to JSON-serializable format
    json_persons = json.loads(json_util.dumps(persons))
    return jsonify(json_persons), 200


# Read Person by ID
@person_routes.route("/<person_id>", methods=["GET"])
def get_person(person_id):
    person = Person.find_by_id(person_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404

    # Convert MongoDB object to JSON-serializable format
    json_person = json.loads(json_util.dumps(person))
    return jsonify(json_person), 200


# Delete Person by ID
@person_routes.route("/<person_id>", methods=["DELETE"])
def delete_person(person_id):
    result = Person.delete(person_id)

    if result.deleted_count > 0:
        return jsonify({"message": "Person deleted"}), 200
    return jsonify({"error": "Person not found"}), 404


# Update Person by ID
@person_routes.route("/<person_id>", methods=["PUT"])
def update_person(person_id):
    data = request.json
    result = Person.update(person_id, data)

    if result.modified_count > 0:
        return jsonify({"message": "Person updated"}), 200
    return jsonify({"error": "Person not found"}), 404
