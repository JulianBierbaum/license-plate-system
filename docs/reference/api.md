# API Reference

This document provides a reference for the API endpoints available in the **License Plate System**.

---

## Data Collection Service

The **Data Collection Service** is responsible for receiving vehicle detection data and saving it in the database.

#### `GET /health`

Check the health of the service. This endpoint is used by Docker's health check.

**Response:**
Returns a `200 OK` with a simple JSON body.
```json
{
  "status": "ok"
}
```

---

#### `POST /api/vehicle_detected`

Submit vehicle detection data.

??? example "Request Body"
    ```json
    {
      "camera": "string"
    }
    ```

    **Fields**

    | Name     | Type   | Description                                   |
    |-----------|--------|-----------------------------------------------|
    | `camera`  | string | The name of the camera that detected the vehicle. |

---

## Notification Service

The **Notification Service** manages user preferences for notifications.

#### `GET /health`

Check the health of the service. This endpoint is used by Docker's health check.

**Response:**
Returns a `200 OK` with a simple JSON body.
```json
{
  "status": "ok"
}
```

### User Preferences

#### `POST /user_preferences/`

Create new user preferences.

??? example "Request Body"
    ```json
    {
      "name": "John Doe",
      "email": "john@example.com",
      "notifications_enabled": true
    }
    ```

    **Fields**

    | Name                   | Type  | Description                                   |
    |------------------------|-------|-----------------------------------------------|
    | `name`                 | string | The name of the user.                        |
    | `email`                | string | The email address of the user.               |
    | `notifications_enabled`| bool   | Whether notifications are enabled.           |

**Response:**  
Returns the newly created user preferences record.

---

#### `GET /user_preferences/`

Retrieve all user preferences records.

**Response:**  
Returns a list of all user preferences records.

---

#### `GET /user_preferences/{entry_id}`

Retrieve user preferences by ID.

| Parameter | Type | Description |
|------------|------|-------------|
| `entry_id` | int  | The ID of the user preferences to retrieve. |

**Response:**  
Returns the requested user preferences record.

---

#### `GET /user_preferences/by-name/{name}`

Retrieve user preferences by name.

| Parameter | Type | Description |
|------------|------|-------------|
| `name` | string | The name of the user to retrieve preferences for. |

**Response:**  
Returns the requested user preferences record.

---

#### `PUT /user_preferences/{entry_id}`

Update user preferences by ID.

| Parameter | Type | Description |
|------------|------|-------------|
| `entry_id` | int  | The ID of the user preferences to update. |

??? example "Request Body"
    ```json
    {
      "name": "Jane Doe",
      "email": "jane@example.com",
      "notifications_enabled": false
    }
    ```

    **Fields (all optional)**

    | Name | Type | Description |
    |------|------|-------------|
    | `name` | string | The name of the user. |
    | `email` | string | The email address of the user. |
    | `notifications_enabled` | bool | Whether notifications are enabled. |

**Response:**  
Returns the updated user preferences record.
