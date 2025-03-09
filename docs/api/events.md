### Events API

#### Base path: `/events`

| Method | Endpoint             | Description                                |
| ------ | -------------------- | ------------------------------------------ |
| GET    | `/events/test`       | Test endpoint to verify API is functioning |
| GET    | `/events/all`        | Retrieve all events                        |
| GET    | `/events/{event_id}` | Retrieve a specific event by ID            |
| POST   | `/events/`           | Create a new event                         |
| PUT    | `/events/{event_id}` | Update an existing event                   |
| DELETE | `/events/{event_id}` | Delete an event                            |

#### GET `/events/all`

Returns a list of all events in the database.

**Response (200 OK)**

```json
[
  {
    "_id": {"$oid": "67ccb23d68c963c3a7cbd456"},
    "title": "Initial Report",
    "description": "Victim reported theft of wallet",
    "datetime": "2025-01-01 10:00:00",
    "location": "Central District",
    ...
  },
  ...
]
```

#### GET `/events/{event_id}`

Returns a specific event by ID.

**Parameters**

- `event_id`: MongoDB ObjectId of the event

**Response (200 OK)**

```json
{
  "_id": {"$oid": "67ccb23d68c963c3a7cbd456"},
  "title": "Initial Report",
  "description": "Victim reported theft of wallet",
  "datetime": "2025-01-01 10:00:00",
  "location": "Central District",
  ...
}
```

**Response (404 Not Found)**

```json
{
  "error": "Event not found"
}
```

#### POST `/events/`

Creates a new event.

**Request Body**

```json
{
  "title": "Initial Report",
  "description": "Victim reported theft of wallet",
  "datetime": "2025-01-01 10:00:00",
  "location": "Central District",
  "people_involved": ["67ccb23d68c963c3a7cbd123"],
  "evidence_collected": []
}
```

**Response (201 Created)**

```json
{
  "event_id": "67ccb23d68c963c3a7cbd456"
}
```

#### PUT `/events/{event_id}`

Updates an existing event.

**Parameters**

- `event_id`: MongoDB ObjectId of the event

**Request Body**

```json
{
  "description": "Updated description of the event",
  "evidence_collected": ["67ccb23d68c963c3a7cbd789"]
}
```

**Response (200 OK)**

```json
{
  "message": "Event updated"
}
```

**Response (404 Not Found)**

```json
{
  "error": "Event not found"
}
```

#### DELETE `/events/{event_id}`

Deletes an event.

**Parameters**

- `event_id`: MongoDB ObjectId of the event

**Response (200 OK)**

```json
{
  "message": "Event deleted"
}
```

**Response (404 Not Found)**

```json
{
  "error": "Event not found"
}
```
