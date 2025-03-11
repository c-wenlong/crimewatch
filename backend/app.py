from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1>Hello, World!</h1>"


from mongodb import person_routes
from mongodb import case_routes
from mongodb import event_routes
from mongodb import evidence_routes
from pineconedb import pinecone_case_routes
from pineconedb import pinecone_event_routes
from pineconedb import pinecone_person_routes
from pineconedb import pinecone_evidence_routes

# Register the routes for each entity
app.register_blueprint(person_routes, url_prefix="/people")
app.register_blueprint(case_routes, url_prefix="/cases")
app.register_blueprint(event_routes, url_prefix="/events")
app.register_blueprint(evidence_routes, url_prefix="/evidence")

app.register_blueprint(pinecone_case_routes, url_prefix="/pinecone_cases")
app.register_blueprint(pinecone_event_routes, url_prefix="/pinecone_event")
app.register_blueprint(pinecone_person_routes, url_prefix="/pinecone_person")
app.register_blueprint(pinecone_evidence_routes, url_prefix="/pinecone_evidence")

if __name__ == "__main__":
    app.run(debug=True)
