from flask import Blueprint, request, jsonify
import json
import requests
from bson import json_util
from pineconedb.client import upsert_into_namespace, query_namespace

# Create a Blueprint for Case Routes
pinecone_case_routes = Blueprint("pinecone_case_routes", __name__)

PINECONE_NAMESPACE = "case"

# Upsert Case
@pinecone_case_routes.route("/<case_id>", methods=["POST"])
def upsert_case(case_id):
    response = requests.get(f"http://localhost:5000/cases/caseID/{case_id}")

    response_json = response.json()
    json_case = {}
    json_case['_id'] = response_json['_id']['$oid']
    json_case['chunk_text'] = response_json['description']
    json_case['location'] = response_json['reported_location']
    json_case['title'] = response_json['title']
    json_case['type'] = response_json['type_of_crime']
    json_case['case_id'] = response_json['case_id']

    upsert_into_namespace(PINECONE_NAMESPACE, [json_case])

    return jsonify({"case_id": str(case_id)}), 201

# Query Case
@pinecone_case_routes.route("/<query>", methods=["GET"])
def query_case(query):
    response = query_namespace(PINECONE_NAMESPACE, query)
    return jsonify({"results": response['result']['hits']}), 200

