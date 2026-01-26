from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.user_preferences import UserPreferences


def create_user_preference_entry(db: Session, name: str, email: str) -> UserPreferences:
    """Helper to create a UserPreferences entry directly in the DB for testing."""
    user_pref = UserPreferences(
        name=name,
        email=email,
        receive_alerts=True,
        receive_updates=False,
    )
    db.add(user_pref)
    db.flush()
    db.refresh(user_pref)
    return user_pref


def test_create_user_preferences_success(client: TestClient):
    """
    Test successful creation of user preferences via API.
    """
    response = client.post(
        '/api/user_preferences/',
        json={'name': 'api_user', 'email': 'api@example.com', 'receive_alerts': True, 'receive_updates': True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'api_user'
    assert data['email'] == 'api@example.com'
    assert data['receive_alerts'] is True
    assert data['receive_updates'] is True
    assert 'id' in data


def test_create_user_preferences_duplicate_name(client: TestClient, db: Session):
    """
    Test that creating a user with a duplicate name via API fails.
    """
    create_user_preference_entry(db, 'duplicate_api_user', 'unique@example.com')
    response = client.post(
        '/api/user_preferences/',
        json={'name': 'duplicate_api_user', 'email': 'another@example.com'},
    )
    assert response.status_code == 400


def test_get_all_user_preferences(client: TestClient, db: Session):
    """
    Test retrieving all user preferences via API.
    """
    create_user_preference_entry(db, 'api_user1', 'api1@example.com')
    create_user_preference_entry(db, 'api_user2', 'api2@example.com')

    response = client.get('/api/user_preferences/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_get_user_preferences_by_id_success(client: TestClient, db: Session):
    """
    Test retrieving a specific user preference by ID via API.
    """
    user_pref = create_user_preference_entry(db, 'get_by_id_user', 'get_id@example.com')
    response = client.get(f'/api/user_preferences/{user_pref.id}')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'get_by_id_user'


def test_get_user_preferences_by_id_not_found(client: TestClient):
    """
    Test that retrieving a non-existent user by ID returns 404.
    """
    response = client.get('/api/user_preferences/99999')
    assert response.status_code == 404


def test_get_user_preferences_by_name_success(client: TestClient, db: Session):
    """
    Test retrieving a specific user preference by name via API.
    """
    name = 'get_by_name_user'
    create_user_preference_entry(db, name, 'get_name@example.com')
    response = client.get(f'/api/user_preferences/by-name/{name}')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == name


def test_get_user_preferences_by_name_not_found(client: TestClient):
    """
    Test that retrieving a non-existent user by name returns 404.
    """
    response = client.get('/api/user_preferences/by-name/nonexistent')
    assert response.status_code == 404


def test_update_user_preferences_success(client: TestClient, db: Session):
    """
    Test successful update of a user preference via API.
    """
    user_pref = create_user_preference_entry(db, 'user_to_update', 'update_me@example.com')
    response = client.put(
        f'/api/user_preferences/{user_pref.id}',
        json={'name': 'updated_name', 'email': 'updated@example.com', 'receive_alerts': False},
    )
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'updated_name'
    assert data['email'] == 'updated@example.com'
    assert data['receive_alerts'] is False


def test_update_user_preferences_not_found(client: TestClient):
    """
    Test that updating a non-existent user returns 404.
    """
    response = client.put(
        '/api/user_preferences/99999',
        json={'name': 'new_name'},
    )
    assert response.status_code == 404


def test_update_user_preferences_duplicate_name(client: TestClient, db: Session):
    """
    Test that updating a user to have a duplicate name fails.
    """
    create_user_preference_entry(db, 'existing_name_for_put', 'existing_put@example.com')
    user_to_update = create_user_preference_entry(db, 'user_to_update_put', 'update_me_put@example.com')

    response = client.put(
        f'/api/user_preferences/{user_to_update.id}',
        json={'name': 'existing_name_for_put'},
    )
    assert response.status_code == 400


def test_delete_user_preferences_success(client: TestClient, db: Session):
    """
    Test successful deletion of user preferences.
    """
    user_pref = create_user_preference_entry(db, 'user_to_delete', 'delete_me@example.com')
    response = client.delete(f'/api/user_preferences/{user_pref.id}')
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f'/api/user_preferences/{user_pref.id}')
    assert response.status_code == 404


def test_delete_user_preferences_not_found(client: TestClient):
    """
    Test that deleting a non-existent user returns 404.
    """
    response = client.delete('/api/user_preferences/99999')
    assert response.status_code == 404


def test_create_user_preferences_duplicate_email(client: TestClient, db: Session):
    """
    Test that creating a user with a duplicate email via API fails.
    """
    create_user_preference_entry(db, 'first_user_email', 'duplicate@example.com')
    response = client.post(
        '/api/user_preferences/',
        json={'name': 'second_user_email', 'email': 'duplicate@example.com'},
    )
    assert response.status_code == 400
