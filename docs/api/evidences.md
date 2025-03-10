```markdown
# Evidence API Documentation

## Base Path: `/evidence`

### Endpoints

| Method | Endpoint                     | Description                                     |
|--------|------------------------------|-------------------------------------------------|
| GET    | `/evidence/test`             | Test endpoint to verify API is functioning     |
| GET    | `/evidence/all`              | Retrieve all evidence records                  |
| GET    | `/evidence/{evidence_id}`    | Retrieve a specific evidence record by ID      |
| POST   | `/evidence/`                 | Upload a new evidence file                     |
| PUT    | `/evidence/{evidence_id}`    | Update an existing evidence record             |
| DELETE | `/evidence/{evidence_id}`    | Delete an evidence record                      |
| GET    | `/evidence/download/{evidence_id}` | Download an evidence file                 |

---

## **GET** `/evidence/test`

### Description
A simple test endpoint to check if the API is functional.

### Response (200 OK)
```
this is a test for the evidence route
```

---

## **GET** `/evidence/all`

### Description
Retrieves all evidence records from the database.

### Response (200 OK)
```json
[
  {
    "_id": {"$oid": "67ccb23d68c963c3a7cbd07b"},
    "filename": "evidence_report.pdf",
    "description": "A PDF report containing case details",
    "extracted_text": "Theft was reported in Central District...",
    "file": "Binary data"
  },
  ...
]
```

### Response (404 Not Found)
```json
{
  "error": "Evidence not found"
}
```

---

## **GET** `/evidence/{evidence_id}`

### Description
Retrieves a specific evidence record by ID.

### Parameters
- `evidence_id` (string): MongoDB ObjectId of the evidence record.

### Response (200 OK)
```json
{
  "_id": {"$oid": "67ccb23d68c963c3a7cbd07b"},
  "filename": "evidence_report.pdf",
  "description": "A PDF report containing case details",
  "extracted_text": "Theft was reported in Central District...",
  "file": "Binary data"
}
```

### Response (404 Not Found)
```json
{
  "error": "Evidence not found"
}
```

---

## **POST** `/evidence/`

### Description
Uploads a new evidence file.

### Request Body (Multipart Form)
- `file` (required): The file to be uploaded (`.txt`, `.pdf`, or `.docx`).
- `description` (optional): A description of the evidence.

### Response (201 Created)
```json
{
  "message": "Text extracted and stored successfully"
}
```

### Response (400 Bad Request)
```json
{
  "error": "No file part"
}
```
```json
{
  "error": "File type is not allowed"
}
```

---

## **PUT** `/evidence/{evidence_id}`

### Description
Updates an existing evidence record.

### Parameters
- `evidence_id` (string): MongoDB ObjectId of the evidence record.

### Request Body
```json
{
  "description": "Updated evidence description"
}
```

### Response (200 OK)
```json
{
  "message": "Evidence updated"
}
```

### Response (404 Not Found)
```json
{
  "error": "Evidence not found"
}
```

---

## **DELETE** `/evidence/{evidence_id}`

### Description
Deletes an evidence record.

### Parameters
- `evidence_id` (string): MongoDB ObjectId of the evidence record.

### Response (200 OK)
```json
{
  "message": "Evidence deleted"
}
```

### Response (404 Not Found)
```json
{
  "error": "Evidence not found"
}
```

---

## **GET** `/evidence/download/{evidence_id}`

### Description
Downloads an evidence file.

### Parameters
- `evidence_id` (string): MongoDB ObjectId of the evidence record.

### Response (200 OK)
- Returns the file as a binary stream.

### Response (404 Not Found)
```json
{
  "error": "Evidence document not found"
}
```

### Response (500 Internal Server Error)
```json
{
  "error": "An error occurred while retrieving the file"
}
```
```