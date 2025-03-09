from .case import case_routes
from .event import event_routes
from .person import person_routes
from .client import get_case_collection, get_person_collection, get_event_collection

__all__ = [
    "case_routes",
    "event_routes",
    "person_routes",
    "get_case_collection",
    "get_person_collection",
    "get_event_collection",
]
