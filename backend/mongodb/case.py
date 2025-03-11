from flask import Blueprint, request, jsonify
from models import Case
import json
from bson import json_util

# Create a Blueprint for Case Routes
case_routes = Blueprint("case_routes", __name__)


# Create Case
@case_routes.route("/", methods=["POST"])
def create_case():
    data = request.json
    case = Case(**data)
    case_id = case.save()
    return jsonify({"case_id": str(case_id)}), 201


# Test Case Route
@case_routes.route("/test", methods=["GET"])
def test_case():
    return "this is a test for the case route"


# Get all Cases
@case_routes.route("/all", methods=["GET"])
def get_all_cases():
    cases = Case.find_all()
    if cases is None:
        return jsonify({"error": "Case not found"}), 404

    # Convert MongoDB objects to JSON-serializable format
    json_cases = json.loads(json_util.dumps(cases))
    return jsonify(json_cases), 200


# Read Case by ID
@case_routes.route("/<case_id>", methods=["GET"])
def get_case(case_id):
    case = Case.find_by_id(case_id)
    if case is None:
        return jsonify({"error": "Case not found"}), 404

    # Convert MongoDB object to JSON-serializable format
    json_case = json.loads(json_util.dumps(case))
    return jsonify(json_case), 200

# Read Case by Case ID
@case_routes.route("/caseID/<case_id>", methods=["GET"])
def get_case_by_case_id(case_id):
    case = Case.find_by_case_id(case_id)
    if case is None:
        return jsonify({"error": "Case not found"}), 404

    # Convert MongoDB object to JSON-serializable format
    json_case = json.loads(json_util.dumps(case))
    return jsonify(json_case), 200

# Delete Case by ID
@case_routes.route("/<case_id>", methods=["DELETE"])
def delete_case(case_id):
    result = Case.delete(case_id)

    if result.deleted_count > 0:
        return jsonify({"message": "Case deleted"}), 200
    return jsonify({"error": "Case not found"}), 404


# Update Case by ID
@case_routes.route("/<case_id>", methods=["PUT"])
def update_case(case_id):
    data = request.json
    result = Case.update(case_id, data)

    if result and result.modified_count > 0:
        return jsonify({"message": "Case updated"}), 200
    return jsonify({"error": "Case not found"}), 404
