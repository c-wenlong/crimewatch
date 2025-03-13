from flask import Blueprint, request, jsonify
import json
import requests
from bson import json_util
from chatgpt.client import get_keywords, get_case_vectors, get_evidence_vectors, get_summary

# Create a Blueprint for ChatGPT Routes
chatgpt_routes = Blueprint("chatgpt_routes", __name__)


@chatgpt_routes.route("/", methods=["POST"])
def handle_user_prompt():
    data = request.json
    print(data)
    keywords = get_keywords(data['user_prompt'])
    print(keywords)
    case_vectors = get_case_vectors(keywords)
    print(case_vectors)
    for vector in case_vectors['results']: #do we want to limit to only first case returned
        case_id = vector['fields']['case_id']
        response = requests.get(f"http://localhost:5000/cases/caseID/{case_id}")
        response_json = response.json()
        case_description = response_json['description']
        case_title = response_json['title']
        case_type = response_json['type_of_crime']
        case_location = response_json['reported_location']
        event_ids = response_json['event_ids']
        evidence = response_json['evidence']
        events = []
        # for event_id in event_ids:
        #     event_response = requests.get(f"http://localhost:5000/event/{event_id}")
        #     event_response_json = event_response.json()
        #     event = {
        #         "event_type":event_response_json['event_type'],
        #         "event_description":event_response_json['description'],
        #         "event_location":event_response_json['location'],
        #         "event_reported_by":event_response_json['reported_by'],
        #         "event_occured_at":event_response_json['occured_at'],
        #         "event_reported_at":event_response_json['reported_at'],
        #     }
        #     events.append(event)
        evidence_chunks = []
        # for evidence_id in evidence:
        #     evidence_vectors = get_evidence_vectors(keywords, evidence_id['$oid'])
        #     for vector in evidence_vectors['results']:
        #         evidence_chunks.append(vector['chunk_text'])

        enrichment_data = {
            "case_id": case_id,
            "case_description":case_description,
            "case_title":case_title,
            "case_type":case_type,
            "case_location":case_location,
            "events":events,
            "evidence": evidence_chunks
        }
        print(enrichment_data)
        summary = get_summary(data['user_prompt'], json.dumps(enrichment_data))
        return jsonify({"results": summary}), 200

