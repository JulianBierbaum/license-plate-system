# API Reference

This document provides a reference for the API endpoints available in the License Plate System.

## Data Collection Service

The Data Collection Service is responsible for receiving vehicle detection data.

### `POST /api/vehicle_detected`

This endpoint is used to submit vehicle detection data.

**Request Body:**

The request body should be a JSON object with the following structure:

```json
{
  "camera": "string"
}
```

-   `camera` (str): The name of the camera that detected the vehicle.

## Notification Service

The Notification Service is responsible for managing user preferences for notifications.

### User Preferences

#### `POST /user_preferences/`

Create new user preferences.

**Request Body:**

-   `name` (str): The name of the user.
-   `email` (str): The email address of the user.
-   `notifications_enabled` (bool): Whether notifications are enabled for the user.

**Response:**

Returns the newly created user preferences record.

#### `GET /user_preferences/`

Retrieve all user preferences records.

**Response:**

Returns a list of all user preferences records.

#### `GET /user_preferences/{entry_id}`

Retrieve user preferences by ID.

**Path Parameters:**

-   `entry_id` (int): The ID of the user preferences to retrieve.

**Response:**

Returns the requested user preferences record.

#### `GET /user_preferences/by-name/{name}`

Retrieve user preferences by name.

**Path Parameters:**

-   `name` (str): The name of the user to retrieve preferences for.

**Response:**

Returns the requested user preferences record.

#### `PUT /user_preferences/{entry_id}`

Update user preferences by ID.

**Path Parameters:**

-   `entry_id` (int): The ID of the user preferences to update.

**Request Body:**

-   `name` (str, optional): The name of the user.
-   `email` (str, optional): The email address of the user.
-   `notifications_enabled` (bool, optional): Whether notifications are enabled for the user.

**Response:**

Returns the updated user preferences record.