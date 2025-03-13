from flask import Blueprint, request, jsonify
import json
import requests
from bson import json_util
from pineconedb.client import upsert_into_namespace, query_namespace

# Create a Blueprint for Person Routes
pinecone_evidence_routes = Blueprint("pinecone_evidence_routes", __name__)

PINECONE_NAMESPACE = "evidence"

@pinecone_evidence_routes.route("/<evidence_id>", methods=["POST"])
def upsert_evidence(evidence_id):
    print(f"Received Pinecone upsert request for evidence ID: {evidence_id}")
    try:
        # Get payload directly from the POST request
        data = request.json
        if not data:
            return jsonify({"error": "No evidence data provided"}), 400

        # Prepare base evidence metadata using the provided payload
        evidence_metadata = {
            'id': evidence_id,
            'description': data.get('description', ''),
            'filename': data.get('filename', ''),
            'filepath': data.get('filepath', '/placeholder/filepath/'),
            'type': 'evidence'
        }
        
        # Extract text content from the payload
        extracted_content = data.get('extracted_content', '')
        
        # Always expect a "chunks" field in the payload.
        # If it is empty or not provided, treat the whole text as a single chunk.
        chunks = data.get('chunks', [])
        if not chunks:
            chunks = [extracted_content]
        
        print(f"Processing {len(chunks)} chunks for evidence ID: {evidence_id}")
        
        # Prepare records (one per chunk)
        records_to_upsert = []
        for i, chunk in enumerate(chunks):
            record = {
                '_id': f"{evidence_id}_chunk_{i}",
                'chunk_text': chunk,
                'description': evidence_metadata['description'],
                'filename': evidence_metadata['filename'],
                'filepath': evidence_metadata['filepath'],
                'parent_id': evidence_id,
                'chunk_index': i,
                'total_chunks': len(chunks)
            }
            records_to_upsert.append(record)
        
        print(f"Upserting {len(records_to_upsert)} records to Pinecone namespace: {PINECONE_NAMESPACE}")
        upsert_into_namespace(PINECONE_NAMESPACE, records_to_upsert)        
        return jsonify({"evidence_id": evidence_id, "status": "success"}), 201
    except Exception as e:
        print(f"Exception in Pinecone upsert: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Query Evidence
@pinecone_evidence_routes.route("/<query>", methods=["GET"])
def query_evidence(query):
    response = query_namespace(PINECONE_NAMESPACE, query)
    return jsonify({"results": response['result']['hits']}), 200