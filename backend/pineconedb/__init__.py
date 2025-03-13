from .case import pinecone_case_routes
from .event import pinecone_event_routes
from .person import pinecone_person_routes
from .evidence import pinecone_evidence_routes
from .client import (
    upsert_into_namespace,
    query_namespace,
)

__all__ = [
    "pinecone_case_routes",
    "pinecone_event_routes",
    "pinecone_person_routes",
    "pinecone_evidence_routes"
    "upsert_into_namespace",
    "query_namespace",
]
