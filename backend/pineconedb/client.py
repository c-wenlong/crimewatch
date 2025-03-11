from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

try:
    PINECONE_API = os.getenv("PINECONE_API")
    client = Pinecone(api_key=PINECONE_API)

    PINECONE_INDEX = os.getenv("PINECONE_INDEX")
    index = client.Index(PINECONE_INDEX)

except Exception as e:
    raise Exception(f"🚨 Failed to connect to Pinecone DB: {e}")

def upsert_into_namespace(namespace, data):
    index.upsert_records(namespace, data)

def query_namespace(namespace, query):
    results = index.search(
    namespace=namespace,
    query={
            "top_k": 50,
            "inputs": {
                'text': query
            }
        }
    )

    # print(results['result'])
    return results.to_dict()
