from flask import Blueprint, request, jsonify
from models import Event

# Create a Blueprint for Event Routes
event_routes = Blueprint("event_routes", __name__)


# Create Event
@event_routes.route("/", methods=["POST"])
def create_event():
    data = request.json
    event = Event(**data)
    event_id = event.save()
    return jsonify({"event_id": str(event_id)}), 201


@event_routes.route("/test", methods=["GET"])
def test_event():
    return "this is a test for the event route"


# Read Event by ID
@event_routes.route("/<event_id>", methods=["GET"])
def get_event(event_id):
    event = Event.find_by_id(event_id)
    if event:
        return jsonify(event), 200
    return jsonify({"error": "Event not found"}), 404


# Delete Event by ID
@event_routes.route("/<event_id>", methods=["DELETE"])
def delete_event(event_id):
    result = Event.delete(event_id)
    if result.deleted_count > 0:
        return jsonify({"message": "Event deleted"}), 200
    return jsonify({"error": "Event not found"}), 404
