from flask import Blueprint, request, jsonify, send_file
from models import Evidence
import json
from bson import json_util
from werkzeug.utils import secure_filename
import docx
import io
import pypdf
from pypdf import PdfReader

ALLOWED_EXTENSIONS = {"txt", "pdf", "docx"}

# Create a Blueprint for Evidence Routes
evidence_routes = Blueprint("evidence_routes", __name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_file(file: bytes, type: str):
    try:
        if type == "txt":
            return file.decode()
        elif type == "docx":
            doc = docx.Document(io.BytesIO(file))
            text = ""
            for paragraph in doc.paragraphs:
                print("paragraph", paragraph, flush=True)
                text += paragraph.text + " "
            return text
        elif type == "pdf":
            try:
                p = PdfReader(io.BytesIO(file))
            except Exception as e:
                print("Error reading pdf", e, flush=True)
            # Initialize an empty string to store the extracted text
            extracted_text = ""
            # Iterate through each page in the PDF
            for page_num in range(len(p.pages)):
                # Extract the text from the current page
                text = p.pages[page_num].extract_text()

                # Append the extracted text to our main string
                extracted_text += text

            # Close the PDF file
            p.close()
            return extracted_text
    except Exception as e:
        print("Error extracting filecontents", e)
        return None


# Create Evidence
@evidence_routes.route("/", methods=["POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400
        files = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        # if len(files) == 0 or files.filename == "":
        if not files or not files.filename:
            print(files)
            return jsonify({"error": "No selected file"}), 400

        if allowed_file(files.filename):
            filename = secure_filename(files.filename)
            description = request.form.get("description")
            file = files.read()
            extracted_content = ""
            try:
                if (
                    filename.endswith(".txt")
                    or filename.endswith(".docx")
                    or filename.endswith(".pdf")
                ):
                    print("matches", filename, flush=True)
                    extracted_content = extract_text_from_file(
                        file, filename.rsplit(".", 1)[1]
                    )
            except Exception as e:
                print(f"Error processing {files}: {e}", flush=True)
            evidence = Evidence(filename, description, extracted_content, file)
            evidence.save()
            return jsonify({"message": "Text extracted and stored successfully"}), 201
        else:
            return jsonify({"error": "File type is not allowed"}), 400
    else:
        return jsonify({"error": "Method not allowed"}), 405



# Test Evidence Route
@evidence_routes.route("/test", methods=["GET"])
def test_evidence():
    return "this is a test for the evidence route"


# Get all Evidence
@evidence_routes.route("/all", methods=["GET"])
def get_all_persons():
    evidences = Evidence.find_all()
    if evidences is None:
        return jsonify({"error": "evidence not found"}), 404

    # Convert MongoDB objects to JSON-serializable format
    json_evidences = json.loads(json_util.dumps(evidences))
    return jsonify(json_evidences), 200


# Read Evidence by ID
@evidence_routes.route("/<evidence_id>", methods=["GET"])
def get_evidence(evidence_id):
    evidence = Evidence.find_by_id(evidence_id)
    if evidence is None:
        return jsonify({"error": "Evidence not found"}), 404

    # Convert MongoDB object to JSON-serializable format
    json_evidence = json.loads(json_util.dumps(evidence))
    return jsonify(json_evidence), 200

# Download Evidence
@evidence_routes.route("/download/<evidence_id>", methods=["GET"])
def download_evidence(evidence_id):
    try:
        evidence = Evidence.find_by_id(evidence_id)
        if evidence is not None:
            # Extract the binary data from the "file" field
            file_binary = evidence["file"]
            
            return send_file(io.BytesIO(file_binary), mimetype='application/octet-stream', download_name=evidence["filename"])
        else:
            return "Evidence document not found", 404
    except Exception as e:
        print(e)
        return str(e), 500


# Delete Evidence by ID
@evidence_routes.route("/<evidence_id>", methods=["DELETE"])
def delete_evidence(evidence_id):
    result = Evidence.delete(evidence_id)

    if result.deleted_count > 0:
        return jsonify({"message": "Evidence deleted"}), 200
    return jsonify({"error": "Evidence not found"}), 404


# Update Evidence by ID
@evidence_routes.route("/<evidence_id>", methods=["PUT"])
def update_evidence(evidence_id):
    data = request.json
    result = Evidence.update(evidence_id, data)

    if result.modified_count > 0:
        return jsonify({"message": "Evidence updated"}), 200
    return jsonify({"error": "Evidence not found"}), 404
