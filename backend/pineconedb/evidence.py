from flask import Blueprint, request, jsonify
import json
import requests
from bson import json_util
from pineconedb.client import upsert_into_namespace, query_namespace

# Create a Blueprint for Person Routes
pinecone_evidence_routes = Blueprint("pinecone_evidence_routes", __name__)

PINECONE_NAMESPACE = "evidence"

# Upsert Evidence
@pinecone_evidence_routes.route("/<evidence_id>", methods=["POST"])
def upsert_evidence(evidence_id):
    response = requests.get(f"http://localhost:5000/evidence/{evidence_id}")

    response_json = response.json()
    json_evidence = {}
    json_evidence['_id'] = response_json['_id']['$oid']
    json_evidence['chunk_text'] = response_json['extracted_content']
    json_evidence['description'] = response_json['description']
    json_evidence['filename'] = response_json['filename']
    json_evidence['filepath'] = '/placeholder/filepath/' #response_json['filepath']

    upsert_into_namespace(PINECONE_NAMESPACE, [json_evidence])

    return jsonify({"evidence_id": str(evidence_id)}), 201

# Query Evidence
@pinecone_evidence_routes.route("/<evidence_id>", methods=["GET"])
def query_evidence(evidence_id):
    query = PINECONE_NAMESPACE + " " + evidence_id
    response = query_namespace(PINECONE_NAMESPACE, query)
    return jsonify({"results": response['result']['hits']}), 200

