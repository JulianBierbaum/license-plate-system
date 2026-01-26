from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.user_preferences import UserPreferences


def create_user_preference_entry(
    db: Session, name: str, email: str, receive_alerts: bool = False, receive_updates: bool = False
) -> UserPreferences:
    """Helper to create a UserPreferences entry directly in the DB for testing."""
    user_pref = UserPreferences(
        name=name,
        email=email,
        receive_alerts=receive_alerts,
        receive_updates=receive_updates,
    )
    db.add(user_pref)
    db.flush()
    db.refresh(user_pref)
    return user_pref


class TestSendNotification:
    """Tests for POST /api/notifications/send endpoint"""

    def test_send_alert_to_all_alert_subscribers(self, client: TestClient, db: Session):
        """Test sending alert to all users with receive_alerts=True"""
        # Create users with different preferences
        create_user_preference_entry(db, 'alert_user1', 'alert1@example.com', receive_alerts=True)
        create_user_preference_entry(db, 'alert_user2', 'alert2@example.com', receive_alerts=True)
        create_user_preference_entry(db, 'no_alert_user', 'noalert@example.com', receive_alerts=False)

        with patch('src.api.routes.notifications.email_handler') as mock_handler:
            mock_handler.send_alert.return_value = {
                'alert1@example.com': True,
                'alert2@example.com': True,
            }

            response = client.post(
                '/api/notifications/send',
                json={
                    'notification_type': 'alert',
                    'subject': 'Test Alert',
                    'body': 'This is a test alert',
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data['total_recipients'] == 2
            assert data['successful'] == 2
            assert data['failed'] == 0

    def test_send_update_to_all_update_subscribers(self, client: TestClient, db: Session):
        """Test sending update to all users with receive_updates=True"""
        create_user_preference_entry(db, 'update_user1', 'update1@example.com', receive_updates=True)
        create_user_preference_entry(db, 'no_update_user', 'noupdate@example.com', receive_updates=False)

        with patch('src.api.routes.notifications.email_handler') as mock_handler:
            mock_handler.send_update.return_value = {'update1@example.com': True}

            response = client.post(
                '/api/notifications/send',
                json={
                    'notification_type': 'update',
                    'subject': 'Test Update',
                    'body': 'This is a test update',
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data['total_recipients'] == 1
            assert data['successful'] == 1

    def test_send_notification_to_specific_recipients(self, client: TestClient, db: Session):
        """Test sending notification to specific users by name"""
        create_user_preference_entry(db, 'target_user', 'target@example.com', receive_alerts=True)
        create_user_preference_entry(db, 'other_user', 'other@example.com', receive_alerts=True)

        with patch('src.api.routes.notifications.email_handler') as mock_handler:
            mock_handler.send_alert.return_value = {'target@example.com': True}

            response = client.post(
                '/api/notifications/send',
                json={
                    'notification_type': 'alert',
                    'subject': 'Targeted Alert',
                    'body': 'This is for specific users',
                    'recipient_names': ['target_user'],
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data['total_recipients'] == 1
            # Only target_user should receive, not other_user

    def test_send_notification_no_recipients(self, client: TestClient, db: Session):
        """Test sending notification when no users match preferences"""
        # Create user with no alerts enabled
        create_user_preference_entry(db, 'no_prefs_user', 'noprefs@example.com', receive_alerts=False)

        response = client.post(
            '/api/notifications/send',
            json={
                'notification_type': 'alert',
                'subject': 'No Recipients',
                'body': 'Nobody will receive this',
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data['total_recipients'] == 0
        assert data['successful'] == 0
        assert data['failed'] == 0

    def test_send_notification_with_partial_failure(self, client: TestClient, db: Session):
        """Test notification response when some emails fail"""
        create_user_preference_entry(db, 'success_user', 'success@example.com', receive_alerts=True)
        create_user_preference_entry(db, 'fail_user', 'fail@example.com', receive_alerts=True)

        with patch('src.api.routes.notifications.email_handler') as mock_handler:
            mock_handler.send_alert.return_value = {
                'success@example.com': True,
                'fail@example.com': False,
            }

            response = client.post(
                '/api/notifications/send',
                json={
                    'notification_type': 'alert',
                    'subject': 'Partial Failure',
                    'body': 'Some will fail',
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data['total_recipients'] == 2
            assert data['successful'] == 1
            assert data['failed'] == 1

    def test_send_update_to_specific_recipients(self, client: TestClient, db: Session):
        """Test sending update notification to specific users"""
        create_user_preference_entry(db, 'update_target', 'updatetarget@example.com', receive_updates=True)

        with patch('src.api.routes.notifications.email_handler') as mock_handler:
            mock_handler.send_update.return_value = {'updatetarget@example.com': True}

            response = client.post(
                '/api/notifications/send',
                json={
                    'notification_type': 'update',
                    'subject': 'Targeted Update',
                    'body': 'Specific update',
                    'recipient_names': ['update_target'],
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data['total_recipients'] == 1
