from flask import Blueprint, request, jsonify
import json
import requests
from bson import json_util
from chatgpt.client import (
    get_keywords,
    get_case_vectors,
    get_evidence_vectors,
    get_summary,
)
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
    print(data)
    case_context = data["case_context"]
    # keywords = get_keywords(data['user_prompt'])
    # print(keywords)
    # case_vectors = get_case_vectors(keywords)
    # print(case_vectors)
    # for vector in case_vectors['results']: #do we want to limit to only first case returned
    case_id = case_context["case_id"]
    response = requests.get(f"{APP_URI}/cases/caseID/{case_id}")
    response_json = response.json()
    print(response.json)
    case_description = response_json["description"]
    case_title = response_json["title"]
    case_type = response_json["type_of_crime"]
    case_location = response_json["reported_location"]
    event_ids = response_json["event_ids"]
    evidence = response_json["evidence"]
    events = []
    for event_id in event_ids:
        event_response = requests.get(f"{APP_URI}/event/{event_id}")
        event_response_json = event_response.json()
        event = {
            "event_type": event_response_json["event_type"],
            "event_description": event_response_json["description"],
            "event_location": event_response_json["location"],
            "event_reported_by": event_response_json["reported_by"],
            "event_occured_at": event_response_json["occured_at"],
            "event_reported_at": event_response_json["reported_at"],
        }
        events.append(event)
    evidence_chunks = []
    for evidence_id in evidence:
        evidence_vectors = get_evidence_vectors(case_context, evidence_id["$oid"])
        for vector in evidence_vectors["results"]:
            evidence_chunks.append(vector["chunk_text"])

    enrichment_data = {
        "case_id": case_id,
        "case_description": case_description,
        "case_title": case_title,
        "case_type": case_type,
        "case_location": case_location,
        "events": events,
        "evidence": evidence_chunks,
    }
    print(enrichment_data)
    summary = get_summary(data["user_prompt"], json.dumps(enrichment_data))
    return jsonify({"results": summary}), 200
