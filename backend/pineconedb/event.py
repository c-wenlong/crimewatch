from flask import Blueprint, request, jsonify
import json
import requests
from bson import json_util
from pineconedb.client import upsert_into_namespace, query_namespace

# Create a Blueprint for Event Routes
pinecone_event_routes = Blueprint("pinecone_event_routes", __name__)

PINECONE_NAMESPACE = "event"

# Upsert Event
@pinecone_event_routes.route("/events/<event_id>", methods=["POST"])
def upsert_event(event_id):
    response = requests.get(f"http://localhost:5000/events/{event_id}")

    response_json = response.json()
    json_event = {}
    json_event['_id'] = response_json['_id']['$oid']
    json_event['chunk_text'] = response_json['description']
    json_event['location'] = response_json['location']
    json_event['type'] = response_json['event_type']

    upsert_into_namespace(PINECONE_NAMESPACE, [json_event])

    return jsonify({"event_id": str(event_id)}), 201

# Query Event
@pinecone_event_routes.route("/events/<event_id>", methods=["GET"])
def query_event(event_id):
    query = PINECONE_NAMESPACE + " " + event_id
    response = query_namespace(PINECONE_NAMESPACE, query)
    return jsonify({"results": response['result']['hits']}), 200

