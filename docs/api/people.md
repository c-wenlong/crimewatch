### People API

#### Base path: `/people`

| Method | Endpoint              | Description                                |
| ------ | --------------------- | ------------------------------------------ |
| GET    | `/people/test`        | Test endpoint to verify API is functioning |
| GET    | `/people/all`         | Retrieve all people                        |
| GET    | `/people/{person_id}` | Retrieve a specific person by ID           |
| POST   | `/people/`            | Create a new person                        |
| PUT    | `/people/{person_id}` | Update an existing person                  |
| DELETE | `/people/{person_id}` | Delete a person                            |

#### GET `/people/all`

Returns a list of all people in the database.

**Response (200 OK)**

```json
[
  {
    "_id": {"$oid": "67ccb23d68c963c3a7cbd123"},
    "first_name": "John",
    "last_name": "Doe",
    "role": "Witness",
    ...
  },
  ...
]
```

#### GET `/people/{person_id}`

Returns a specific person by ID.

**Parameters**

- `person_id`: MongoDB ObjectId of the person

**Response (200 OK)**

```json
{
  "_id": {"$oid": "67ccb23d68c963c3a7cbd123"},
  "first_name": "John",
  "last_name": "Doe",
  "role": "Witness",
  ...
}
```

**Response (404 Not Found)**

```json
{
  "error": "Person not found"
}
```

#### POST `/people/`

Creates a new person.

**Request Body**

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "role": "Witness",
  "contact_info": {
    "phone": "555-1234",
    "email": "john.doe@example.com"
  }
}
```

**Response (201 Created)**

```json
{
  "person_id": "67ccb23d68c963c3a7cbd123"
}
```

#### PUT `/people/{person_id}`

Updates an existing person.

**Parameters**

- `person_id`: MongoDB ObjectId of the person

**Request Body**

```json
{
  "role": "Suspect",
  "contact_info": {
    "phone": "555-5678"
  }
}
```

**Response (200 OK)**

```json
{
  "message": "Person updated"
}
```

**Response (404 Not Found)**

```json
{
  "error": "Person not found"
}
```

#### DELETE `/people/{person_id}`

Deletes a person.

**Parameters**

- `person_id`: MongoDB ObjectId of the person

**Response (200 OK)**

```json
{
  "message": "Person deleted"
}
```

**Response (404 Not Found)**

```json
{
  "error": "Person not found"
}
```
