from .case import case_routes
from .event import event_routes
from .person import person_routes
from .evidence import evidence_routes
from .client import get_case_collection, get_person_collection, get_event_collection, get_evidence_collection

__all__ = [
    "case_routes",
    "event_routes",
    "person_routes",
    "evidence_routes",
    "get_case_collection",
    "get_person_collection",
    "get_event_collection",
    "get_evidence_collection",
]
