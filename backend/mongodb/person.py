from flask import Blueprint, request, jsonify
from models import Person

# Create a Blueprint for Person Routes
person_routes = Blueprint("person_routes", __name__)


# Create Person
@person_routes.route("/", methods=["POST"])
def create_person():
    data = request.json
    person = Person(**data)
    person_id = person.save()
    return jsonify({"person_id": str(person_id)}), 201


# Read Person by ID
@person_routes.route("/<person_id>", methods=["GET"])
def get_person(person_id):
    person = Person.find_by_id(person_id)
    if person:
        return jsonify(person), 200
    return jsonify({"error": "Person not found"}), 404


# Delete Person by ID
@person_routes.route("/<person_id>", methods=["DELETE"])
def delete_person(person_id):
    result = Person.delete(person_id)
    if result.deleted_count > 0:
        return jsonify({"message": "Person deleted"}), 200
    return jsonify({"error": "Person not found"}), 404
