### Cases API

#### Base path: `/cases`

| Method | Endpoint           | Description                                |
| ------ | ------------------ | ------------------------------------------ |
| GET    | `/cases/test`      | Test endpoint to verify API is functioning |
| GET    | `/cases/all`       | Retrieve all cases                         |
| GET    | `/cases/{case_id}` | Retrieve a specific case by ID             |
| POST   | `/cases/`          | Create a new case                          |
| PUT    | `/cases/{case_id}` | Update an existing case                    |
| DELETE | `/cases/{case_id}` | Delete a case                              |

#### GET `/cases/all`

Returns a list of all cases in the database.

**Response (200 OK)**

```json
[
  {
    "_id": {"$oid": "67ccb23d68c963c3a7cbd07b"},
    "title": "Theft at Central District",
    "description": "A theft was reported in the Central District. Investigation is ongoing",
    "type_of_crime": "Theft",
    "reported_location": "Central District",
    "reported_datetime": "2025-01-01 10:00:00",
    "people_involved": [...],
    "evidence": [...],
    "events": [...]
  },
  ...
]
```

#### GET `/cases/{case_id}`

Returns a specific case by ID.

**Parameters**

- `case_id`: MongoDB ObjectId of the case

**Response (200 OK)**

```json
{
  "_id": {"$oid": "67ccb23d68c963c3a7cbd07b"},
  "title": "Theft at Central District",
  "description": "A theft was reported in the Central District. Investigation is ongoing",
  "type_of_crime": "Theft",
  "reported_location": "Central District",
  "reported_datetime": "2025-01-01 10:00:00",
  "people_involved": [...],
  "evidence": [...],
  "events": [...]
}
```

**Response (404 Not Found)**

```json
{
  "error": "Case not found"
}
```

#### POST `/cases/`

Creates a new case.

**Request Body**

```json
{
  "title": "Theft at Central District",
  "description": "A theft was reported in the Central District",
  "type_of_crime": "Theft",
  "reported_location": "Central District",
  "reported_datetime": "2025-01-01 10:00:00",
  "investigator_id": "67ccb23d68c963c3a7cbd123",
  "people_involved": [],
  "evidence": [],
  "event_ids": []
}
```

**Response (201 Created)**

```json
{
  "case_id": "67ccb23d68c963c3a7cbd07b"
}
```

#### PUT `/cases/{case_id}`

Updates an existing case.

**Parameters**

- `case_id`: MongoDB ObjectId of the case

**Request Body**

```json
{
  "title": "Updated Theft Case",
  "status": "Closed"
}
```

**Response (200 OK)**

```json
{
  "message": "Case updated"
}
```

**Response (404 Not Found)**

```json
{
  "error": "Case not found"
}
```

#### DELETE `/cases/{case_id}`

Deletes a case.

**Parameters**

- `case_id`: MongoDB ObjectId of the case

**Response (200 OK)**

```json
{
  "message": "Case deleted"
}
```

**Response (404 Not Found)**

```json
{
  "error": "Case not found"
}
```