# CrimeWatch API Documentation

## Overview

This API provides endpoints to manage cases, people, and events for a crime investigation system. All data is stored in MongoDB and served through Flask REST endpoints.

## Base URL

`http://localhost:5000`

## Authentication

Currently, this API does not implement authentication.

## Error Handling

All errors return JSON responses with an "error" field containing a description of the error.

- `404`: Resource not found
- `500`: Server error

## Endpoints

#### Cases

| Method | Endpoint           | Description                                |
| ------ | ------------------ | ------------------------------------------ |
| GET    | `/cases/test`      | Test endpoint to verify API is functioning |
| GET    | `/cases/all`       | Retrieve all cases                         |
| GET    | `/cases/{case_id}` | Retrieve a specific case by ID             |
| POST   | `/cases/`          | Create a new case                          |
| PUT    | `/cases/{case_id}` | Update an existing case                    |
| DELETE | `/cases/{case_id}` | Delete a case                              |

<strong> For details, go to `./cases.md`. </strong>

#### People

| Method | Endpoint              | Description                                |
| ------ | --------------------- | ------------------------------------------ |
| GET    | `/people/test`        | Test endpoint to verify API is functioning |
| GET    | `/people/all`         | Retrieve all people                        |
| GET    | `/people/{person_id}` | Retrieve a specific person by ID           |
| POST   | `/people/`            | Create a new person                        |
| PUT    | `/people/{person_id}` | Update an existing person                  |
| DELETE | `/people/{person_id}` | Delete a person                            |

<strong> For details, go to `./people.md`. </strong>

#### Events

| Method | Endpoint             | Description                                |
| ------ | -------------------- | ------------------------------------------ |
| GET    | `/events/test`       | Test endpoint to verify API is functioning |
| GET    | `/events/all`        | Retrieve all events                        |
| GET    | `/events/{event_id}` | Retrieve a specific event by ID            |
| POST   | `/events/`           | Create a new event                         |
| PUT    | `/events/{event_id}` | Update an existing event                   |
| DELETE | `/events/{event_id}` | Delete an event                            |

<strong> For details, go to `./events.md`. </strong>

## Database Configuration (client.py)

The MongoDB connection is established using environment variables:

- `MONGODB_URI`: The connection string for MongoDB
- `DATABASE_NAME`: The name of the database
- `CASE_COLLECTION`: The name of the collection for cases
- `PERSON_COLLECTION`: The name of the collection for people
- `EVENT_COLLECTION`: The name of the collection for events

These values should be set in a `.env` file in the project root.

## Main Application (app.py)

The main application file configures the Flask app and registers the blueprints for each entity with their respective URL prefixes.
