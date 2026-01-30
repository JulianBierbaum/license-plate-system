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

The **Notification Service** manages user preferences for notifications and sends email alerts/updates.

!!! warning "Authentication Required"
    All notification service endpoints (except `/health`) require an API key. Include the `Authorization` header with your API key:
    ```
    Authorization: your-api-key-here
    ```

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

### User Preferences

#### `POST /api/user_preferences/`

Create new user preferences.

??? example "Request Body"
    ```json
    {
      "name": "John Doe",
      "email": "john@example.com",
      "receive_alerts": true,
      "receive_updates": false
    }
    ```

    **Fields**

    | Name             | Type   | Description                                |
    |------------------|--------|--------------------------------------------|
    | `name`           | string | The name of the user (5-50 chars).         |
    | `email`          | string | The email address of the user.             |
    | `receive_alerts` | bool   | Whether the user receives alert emails.    |
    | `receive_updates`| bool   | Whether the user receives update emails.   |

**Response:**  
Returns the newly created user preferences record.

---

#### `GET /api/user_preferences/`

Retrieve all user preferences records.

**Response:**  
Returns a list of all user preferences records.

---

#### `GET /api/user_preferences/{entry_id}`

Retrieve user preferences by ID.

| Parameter | Type | Description |
|------------|------|-------------|
| `entry_id` | int  | The ID of the user preferences to retrieve. |

**Response:**  
Returns the requested user preferences record, or `404` if not found.

---

#### `GET /api/user_preferences/by-name/{name}`

Retrieve user preferences by name.

| Parameter | Type | Description |
|------------|------|-------------|
| `name` | string | The name of the user to retrieve preferences for. |

**Response:**  
Returns the requested user preferences record, or `404` if not found.

---

#### `PUT /api/user_preferences/{entry_id}`

Update user preferences by ID.

| Parameter | Type | Description |
|------------|------|-------------|
| `entry_id` | int  | The ID of the user preferences to update. |

??? example "Request Body"
    ```json
    {
      "name": "Jane Doe",
      "email": "jane@example.com",
      "receive_alerts": false,
      "receive_updates": true
    }
    ```

    **Fields (all optional)**

    | Name | Type | Description |
    |------|------|-------------|
    | `name` | string | The name of the user. |
    | `email` | string | The email address of the user. |
    | `receive_alerts` | bool | Whether the user receives alerts. |
    | `receive_updates` | bool | Whether the user receives updates. |

**Response:**  
Returns the updated user preferences record, or `404` if not found.

---

#### `DELETE /api/user_preferences/{entry_id}`

Delete user preferences by ID.

| Parameter | Type | Description |
|------------|------|-------------|
| `entry_id` | int  | The ID of the user preferences to delete. |

**Response:**  
Returns `204 No Content` on success, or `404` if not found.

---

### Notifications

#### `POST /api/notifications/send`

Send a notification to users based on their preferences.

??? example "Request Body"
    ```json
    {
      "notification_type": "alert",
      "subject": "Security Alert",
      "body": "Unauthorized vehicle detected",
      "recipients": ["security_team@example.com"],
      "html": false
    }
    ```

    **Fields**

    | Name | Type | Required | Description |
    |------|------|----------|-------------|
    | `notification_type` | string | Yes | Either `"alert"` or `"update"`. Determines which users receive the notification. |
    | `subject` | string | Yes | Email subject (max 200 chars). |
    | `body` | string | Yes | Email body content. |
    | `recipients` | list | No | Optional list of specific email addresses to send to. If omitted, sends to all users with matching preference. |
    | `html` | bool | No | If `true`, send body as HTML. Defaults to `false`. |

??? example "Response"
    ```json
    {
      "total_recipients": 2,
      "successful": 2,
      "failed": 0,
      "results": [
        {"email": "user1@example.com", "success": true},
        {"email": "user2@example.com", "success": true}
      ]
    }
    ```
