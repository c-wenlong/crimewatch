from flask import Blueprint, request, jsonify
import json
import requests
from bson import json_util
from chatgpt.client import (
    get_evidence_vectors,
    get_summary,
)
from models import Case, Event
from dotenv import load_dotenv
import os

load_dotenv()

# Create a Blueprint for ChatGPT Routes
chatgpt_routes = Blueprint("chatgpt_routes", __name__)

APP_URI = os.getenv("APP_URI")


@chatgpt_routes.route("/", methods=["GET"])
def chatgpt_get():
    return jsonify({"message": "ChatGPT endpoint is active."}), 200


@chatgpt_routes.route("/", methods=["POST"])
def handle_user_prompt():
    data = request.json
    case_context = data["case_context"]
    case_id = case_context["case_id"]
    case = Case.find_by_case_id(case_id)
    if case is None:
        return jsonify({"error": "Case not found"}), 404

    # Convert MongoDB object to JSON-serializable format
    json_case = json.loads(json_util.dumps(case))
    case_description = json_case["description"]
    case_title = json_case["title"]
    case_type = json_case["type_of_crime"]
    case_location = json_case["reported_location"]
    event_ids = json_case["event_ids"]
    evidence = json_case["evidence"]
    events = []
    for event_id in event_ids:
        event = Event.find_by_id(event_id)
        if event is None:
            return jsonify({"error": "Event not found"}), 404

        # Convert MongoDB object to JSON-serializable format
        json_event = json.loads(json_util.dumps(event))
        event = {
            "event_type": json_event["event_type"],
            "event_description": json_event["description"],
            "event_location": json_event["location"],
            "event_reported_by": json_event["reported_by"],
            "event_occurred_at": json_event["occurred_at"],
            "event_reported_at": json_event["reported_at"],
        }
        events.append(event)

    evidence_chunks = []
    for evidence_id in evidence:
        evidence_vectors = get_evidence_vectors(case_context, evidence_id["$oid"])
        for vector in evidence_vectors["results"]:
            evidence_chunks.append(vector["fields"]["chunk_text"])

    enrichment_data = {
        "case_id": case_id,
        "case_description": case_description,
        "case_title": case_title,
        "case_type": case_type,
        "case_location": case_location,
        "events": events,
        "evidence": evidence_chunks,
    }
    summary = get_summary(data["user_prompt"], json.dumps(enrichment_data))
    return jsonify({"results": summary}), 200
