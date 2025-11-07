# API Reference

This document provides a reference for the API endpoints available in the **License Plate System**.

---

## Data Collection Service

The **Data Collection Service** is responsible for receiving vehicle detection data and saving it in the database.

- **Base URL**: `http://<host>:<port>`
- **Authentication**: HTTP Basic Authentication

### Authentication

- **How to Authenticate**: Use HTTP Basic Authentication with the username and password provided in the environment variables.
- **API Key / Token Management**: Credentials are managed through environment variables (`SYNOLOGY_USERNAME` and `SYNOLOGY_PASSWORD`).
- **Security Considerations**: It is recommended to use strong, unique passwords and to restrict access to the API endpoint to trusted IP addresses.

### Endpoints

#### `POST /api/vehicle_detected`

This endpoint receives a notification when a vehicle is detected by a camera. It triggers a background task to capture a snapshot from the camera, send it to the Plate Recognizer service, and store the results in the database.

**Authentication Required**: Yes

??? example "Request Body"
    ```json
    {
      "camera": "string"
    }
    ```
    **Fields**

    | Name     | Type   | Required | Description                                   | Example    |
    |----------|--------|----------|-----------------------------------------------|------------|
    | `camera` | string | Yes      | The name of the camera that detected the vehicle. | "Camera 1" |

**Response**:
- **Status Code**: `200 OK`

??? example "Response Body"
    ```json
    {
      "status": "accepted",
      "timestamp": "20231027_100000"
    }
    ```

**Error Responses**:
- `401 Unauthorized`: Incorrect username or password.
- `500 Internal Server Error`: An unexpected error occurred during processing.

### Data Models / Schemas

??? example "TypeScript"
    ```typescript
    interface VehicleDetectionRequest {
      camera: string;
    }
    ```

### Code Examples

??? example "cURL"
    ```bash
    cURL -X POST http://<host>:<port>/api/vehicle_detected \
      -u "username:password" \
      -H "Content-Type: application/json" \
      -d '{"camera": "Camera 1"}'
    ```

??? example "Python"
    ```python
    import requests

    url = "http://<host>:<port>/api/vehicle_detected"
    auth = ("username", "password")
    data = {"camera": "Camera 1"}

    response = requests.post(url, auth=auth, json=data)

    print(response.json())
    ```

??? example "JavaScript/TypeScript"
    ```javascript
    const axios = require('axios');

    const url = 'http://<host>:<port>/api/vehicle_detected';
    const auth = {
      username: 'username',
      password: 'password'
    };
    const data = { camera: 'Camera 1' };

    axios.post(url, data, { auth })
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.error(error.response.data);
      });
    ```

---

## Notification Service

The **Notification Service** is responsible for managing user preferences for notifications.

- **Base URL**: `http://<host>:<port>`
- **Authentication**: None
- **Rate Limits**: Not specified.
- **API Version**: v1

### Endpoints

#### `POST /api/user_preferences/`

Create new user preferences.

**Authentication Required**: No

??? example "Request Body"
    ```json
    {
      "name": "string",
      "email": "string",
      "notification_on_new_plate": true
    }
    ```
    **Fields**

    | Name                        | Type    | Required | Description                         |
    |-----------------------------|---------|----------|-------------------------------------|
    | `name`                      | string  | Yes      | The name of the user.               |
    | `email`                     | string  | Yes      | The email address of the user.      |
    | `notification_on_new_plate` | boolean | Yes      | Whether notifications are enabled.  |

**Response**:
- **Status Code**: `200 OK`

??? example "Response Body"
    ```json
    {
      "id": 0,
      "name": "string",
      "email": "string",
      "notification_on_new_plate": true
    }
    ```

**Error Responses**:
- `400 Bad Request`: User preferences with this name already exist.

#### `GET /api/user_preferences/`

Retrieve all user preferences records.

**Authentication Required**: No

**Response**:
- **Status Code**: `200 OK`

??? example "Response Body"
    ```json
    [
      {
        "id": 0,
        "name": "string",
        "email": "string",
        "notification_on_new_plate": true
      }
    ]
    ```

**Error Responses**:
- `500 Internal Server Error`: Failed to fetch user preferences.

#### `GET /api/user_preferences/{entry_id}`

Retrieve user preferences by ID.

**Authentication Required**: No

**Path Parameters**:
| Parameter | Type    | Required | Description                               |
|-----------|---------|----------|-------------------------------------------|
| `entry_id`| integer | Yes      | The ID of the user preferences to retrieve. |

**Response**:
- **Status Code**: `200 OK`

??? example "Response Body"
    ```json
    {
      "id": 0,
      "name": "string",
      "email": "string",
      "notification_on_new_plate": true
    }
    ```

**Error Responses**:
- `404 Not Found`: User preferences not found.
- `500 Internal Server Error`: Failed to fetch user preferences.

#### `GET /api/user_preferences/by-name/{name}`

Retrieve user preferences by name.

**Authentication Required**: No

**Path Parameters**:
| Parameter | Type   | Required | Description                                     |
|-----------|--------|----------|-------------------------------------------------|
| `name`    | string | Yes      | The name of the user to retrieve preferences for. |

**Response**:
- **Status Code**: `200 OK`

??? example "Response Body"
    ```json
    {
      "id": 0,
      "name": "string",
      "email": "string",
      "notification_on_new_plate": true
    }
    ```

**Error Responses**:
- `404 Not Found`: User preferences not found.
- `500 Internal Server Error`: Failed to fetch user preferences.

#### `PUT /api/user_preferences/{entry_id}`

Update user preferences by ID.

**Authentication Required**: No

**Path Parameters**:
| Parameter | Type    | Required | Description                             |
|-----------|---------|----------|-----------------------------------------|
| `entry_id`| integer | Yes      | The ID of the user preferences to update. |

??? example "Request Body"
    ```json
    {
      "name": "string",
      "email": "string",
      "notification_on_new_plate": false
    }
    ```
    **Fields (all optional)**

    | Name                        | Type    | Description                        |
    |-----------------------------|---------|------------------------------------|
    | `name`                      | string  | The name of the user.              |
    | `email`                     | string  | The email address of the user.     |
    | `notification_on_new_plate` | boolean | Whether notifications are enabled. |

**Response**:
- **Status Code**: `200 OK`

??? example "Response Body"
    ```json
    {
      "id": 0,
      "name": "string",
      "email": "string",
      "notification_on_new_plate": true
    }
    ```

**Error Responses**:
- `400 Bad Request`: User preferences with this name already exist.
- `404 Not Found`: User preferences not found.

### Data Models / Schemas

??? example "TypeScript"
    ```typescript
    interface UserPreference {
      id: number;
      name: string;
      email: string;
      notification_on_new_plate: boolean;
    }

    interface UserPreferencesCreate {
      name: string;
      email: string;
      notification_on_new_plate: boolean;
    }

    interface UserPreferencesUpdate {
      name?: string;
      email?: string;
      notification_on_new_plate?: boolean;
    }
    ```