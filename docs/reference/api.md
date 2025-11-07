# API Reference

This document provides a comprehensive reference for the API endpoints available in the **License Plate System**.

### Data Collection Service

#### `POST /api/vehicle_detected`
**Description**: Submits vehicle detection data from a camera. This endpoint is called by a camera when it detects a vehicle.

**Authentication Required**: Yes (HTTP Basic Auth)

**Request Body**:
```json
{
  "camera": "string"
}
```

| Parameter | Type   | Required | Description                                  | Example        |
|-----------|--------|----------|----------------------------------------------|----------------|
| `camera`  | string | Yes      | The name of the camera that detected the vehicle. | "front-door"   |

**Response**:
- **Status Code**: 200 OK
```json
{
  "status": "accepted",
  "timestamp": "2025-11-07T12:00:00Z"
}
```

**Error Responses**:
- **401 Unauthorized**: Missing or invalid credentials.
- **500 Internal Server Error**: Server error during processing.

??? example "Example Request"
    ```bash
    curl -X POST https://api.example.com/api/vehicle_detected \
      -u "username:password" \
      -H "Content-Type: application/json" \
      -d '{"camera": "driveway"}'
    ```

---

### Notification Service

#### `POST /api/user_preferences/`
**Description**: Creates a new user preference setting.

**Authentication Required**: No

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "receive_alerts": true,
  "receive_updates": false
}
```

| Parameter        | Type    | Required | Description                               |
|------------------|---------|----------|-------------------------------------------|
| `name`           | string  | Yes      | User's name.                              |
| `email`          | string  | Yes      | User's email address.                     |
| `receive_alerts` | boolean | No       | Whether the user should receive alerts.   |
| `receive_updates`| boolean | No       | Whether the user should receive updates.  |

**Response**:
- **Status Code**: 200 OK
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "receive_alerts": true,
  "receive_updates": false,
  "created_at": "2025-11-07T12:00:00Z",
  "updated_at": null
}
```

**Error Responses**:
- **400 Bad Request**: Duplicate entry or database integrity error.

??? example "Example Request"
    ```bash
    curl -X POST https://api.example.com/api/user_preferences/ \
      -H "Content-Type: application/json" \
      -d '{"name": "John Doe", "email": "john.doe@example.com", "receive_alerts": true}'
    ```

#### `GET /api/user_preferences/`
**Description**: Retrieves all user preference settings.

**Authentication Required**: No

**Response**:
- **Status Code**: 200 OK
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "receive_alerts": true,
    "receive_updates": false,
    "created_at": "2025-11-07T12:00:00Z",
    "updated_at": null
  }
]
```

**Error Responses**:
- **500 Internal Server Error**: Failed to fetch user preferences.

??? example "Example Request"
    ```bash
    curl https://api.example.com/api/user_preferences/
    ```

#### `GET /api/user_preferences/{entry_id}`
**Description**: Retrieves a specific user preference setting by its ID.

**Authentication Required**: No

**Path Parameters**:
| Parameter  | Type    | Required | Description                               |
|------------|---------|----------|-------------------------------------------|
| `entry_id` | integer | Yes      | The ID of the user preference to retrieve. |

**Response**:
- **Status Code**: 200 OK
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "receive_alerts": true,
  "receive_updates": false,
  "created_at": "2025-11-07T12:00:00Z",
  "updated_at": null
}
```

**Error Responses**:
- **404 Not Found**: User preference not found.
- **500 Internal Server Error**: Failed to fetch user preferences.

??? example "Example Request"
    ```bash
    curl https://api.example.com/api/user_preferences/1
    ```

#### `GET /api/user_preferences/by-name/{name}`
**Description**: Retrieves a specific user preference setting by name.

**Authentication Required**: No

**Path Parameters**:
| Parameter | Type   | Required | Description                             |
|-----------|--------|----------|-----------------------------------------|
| `name`    | string | Yes      | The name of the user to retrieve for.   |

**Response**:
- **Status Code**: 200 OK
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "receive_alerts": true,
  "receive_updates": false,
  "created_at": "2025-11-07T12:00:00Z",
  "updated_at": null
}
```

**Error Responses**:
- **404 Not Found**: User preference not found.
- **500 Internal Server Error**: Failed to fetch user preferences.

??? example "Example Request"
    ```bash
    curl https://api.example.com/api/user_preferences/by-name/John%20Doe
    ```

#### `PUT /api/user_preferences/{entry_id}`
**Description**: Updates an existing user preference setting.

**Authentication Required**: No

**Path Parameters**:
| Parameter  | Type    | Required | Description                             |
|------------|---------|----------|-----------------------------------------|
| `entry_id` | integer | Yes      | The ID of the user preference to update. |

**Request Body** (all fields are optional):
```json
{
  "name": "Johnathan Doe",
  "email": "john.doe.new@example.com",
  "receive_alerts": false,
  "receive_updates": true
}
```

**Response**:
- **Status Code**: 200 OK
```json
{
  "id": 1,
  "name": "Johnathan Doe",
  "email": "john.doe.new@example.com",
  "receive_alerts": false,
  "receive_updates": true,
  "created_at": "2025-11-07T12:00:00Z",
  "updated_at": "2025-11-07T13:00:00Z"
}
```

**Error Responses**:
- **400 Bad Request**: Duplicate entry or database integrity error.
- **404 Not Found**: User preference not found.

??? example "Example Request"
    ```bash
    curl -X PUT https://api.example.com/api/user_preferences/1 \
      -H "Content-Type: application/json" \
      -d '{"receive_alerts": false}'
    ```
