from flask import Blueprint, request, jsonify
import json
import requests
from bson import json_util
from pineconedb.client import upsert_into_namespace, query_namespace

# Create a Blueprint for Person Routes
pinecone_person_routes = Blueprint("pinecone_person_routes", __name__)

PINECONE_NAMESPACE = "person"

# Upsert Person
@pinecone_person_routes.route("/<person_id>", methods=["POST"])
def upsert_person(person_id):
    response = requests.get(f"http://localhost:5000/person/{person_id}")

    response_json = response.json()
    json_person = {}
    json_person['_id'] = response_json['_id']['$oid']
    json_person['chunk_text'] = response_json['role_in_case']
    json_person['name'] = response_json['name']
    json_person['age'] = response_json['age']
    json_person['gender'] = response_json['gender']
    json_person['known_addresses'] = response_json['known_addresses']

    upsert_into_namespace(PINECONE_NAMESPACE, [json_person])

    return jsonify({"person_id": str(person_id)}), 201

# Query Person
@pinecone_person_routes.route("/<person_id>", methods=["GET"])
def query_person(person_id):
    query = PINECONE_NAMESPACE + " " + person_id
    response = query_namespace(PINECONE_NAMESPACE, query)
    return jsonify({"results": response['result']['hits']}), 200

