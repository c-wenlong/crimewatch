from flask import Blueprint, request, jsonify
from models import Case

# Create a Blueprint for Case Routes
case_routes = Blueprint('case_routes', __name__)

# Create Case
@case_routes.route("/", methods=["POST"])
def create_case():
    data = request.json
    case = Case(**data)
    case_id = case.save()
    return jsonify({"case_id": str(case_id)}), 201

# Read Case by ID
@case_routes.route("/<case_id>", methods=["GET"])
def get_case(case_id):
    case = Case.find_by_id(case_id)
    if case:
        return jsonify(case), 200
    return jsonify({"error": "Case not found"}), 404

# Delete Case by ID
@case_routes.route("/<case_id>", methods=["DELETE"])
def delete_case(case_id):
    result = Case.delete(case_id)
    if result.deleted_count > 0:
        return jsonify({"message": "Case deleted"}), 200
    return jsonify({"error": "Case not found"}), 404
