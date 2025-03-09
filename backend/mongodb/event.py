from flask import Blueprint, request, jsonify
from models import Event
import json
from bson import json_util

# Create a Blueprint for Event Routes
event_routes = Blueprint("event_routes", __name__)


# Create Event
@event_routes.route("/", methods=["POST"])
def create_event():
    data = request.json
    event = Event(**data)
    event_id = event.save()
    return jsonify({"event_id": str(event_id)}), 201


# Get all Events
@event_routes.route("/all", methods=["GET"])
def get_all_events():
    events = Event.find_all()
    if events is None:
        return jsonify({"error": "Event not found"}), 404

    # Convert MongoDB objects to JSON-serializable format
    json_events = json.loads(json_util.dumps(events))
    return jsonify(json_events), 200


# Test Event Route
@event_routes.route("/test", methods=["GET"])
def test_event():
    return "this is a test for the event route"


# Read Event by ID
@event_routes.route("/<event_id>", methods=["GET"])
def get_event(event_id):
    event = Event.find_by_id(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Convert MongoDB object to JSON-serializable format
    json_event = json.loads(json_util.dumps(event))
    return jsonify(json_event), 200


# Delete Event by ID
@event_routes.route("/<event_id>", methods=["DELETE"])
def delete_event(event_id):
    result = Event.delete(event_id)

    if result.deleted_count > 0:
        return jsonify({"message": "Event deleted"}), 200
    return jsonify({"error": "Event not found"}), 404


# Update Event by ID
@event_routes.route("/<event_id>", methods=["PUT"])
def update_event(event_id):
    data = request.json
    result = Event.update(event_id, data)

    if result.modified_count > 0:
        return jsonify({"message": "Event updated"}), 200
    return jsonify({"error": "Event not found"}), 404
