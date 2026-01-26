from unittest.mock import patch, MagicMock

import pytest

from src.handlers.email_handler import EmailSendError


class TestEmailHandler:
    """Tests for EmailHandler class"""

    def test_send_email_success(self, email_handler):
        """Test successful email sending"""
        with patch('src.handlers.email_handler.smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_server)
            mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

            result = email_handler.send_email(
                to='recipient@example.com',
                subject='Test Subject',
                body='Test Body',
            )

            assert result is True
            mock_smtp.assert_called_once_with('test.smtp.local', 25, timeout=30)
            mock_server.sendmail.assert_called_once()

    def test_send_email_smtp_error(self, email_handler):
        """Test email sending with SMTP error"""
        with patch('src.handlers.email_handler.smtplib.SMTP') as mock_smtp:
            import smtplib

            mock_smtp.return_value.__enter__ = MagicMock(side_effect=smtplib.SMTPException('Connection failed'))
            mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

            with pytest.raises(EmailSendError):
                email_handler.send_email(
                    to='recipient@example.com',
                    subject='Test Subject',
                    body='Test Body',
                )

    def test_send_bulk_email_mixed_results(self, email_handler):
        """Test bulk email with some failures"""
        with patch.object(email_handler, 'send_email') as mock_send:
            # First succeeds, second fails
            mock_send.side_effect = [True, EmailSendError('Failed')]

            results = email_handler.send_bulk_email(
                recipients=['success@example.com', 'fail@example.com'],
                subject='Test',
                body='Body',
            )

            assert results['success@example.com'] is True
            assert results['fail@example.com'] is False

    def test_send_alert_adds_prefix(self, email_handler):
        """Test that send_alert adds [ALERT] prefix"""
        with patch.object(email_handler, 'send_bulk_email') as mock_bulk:
            mock_bulk.return_value = {'test@example.com': True}

            email_handler.send_alert(
                recipients=['test@example.com'],
                subject='Important',
                body='Alert body',
            )

            mock_bulk.assert_called_once_with(['test@example.com'], '[ALERT] Important', 'Alert body')

    def test_send_update_adds_prefix(self, email_handler):
        """Test that send_update adds [UPDATE] prefix"""
        with patch.object(email_handler, 'send_bulk_email') as mock_bulk:
            mock_bulk.return_value = {'test@example.com': True}

            email_handler.send_update(
                recipients=['test@example.com'],
                subject='News',
                body='Update body',
            )

            mock_bulk.assert_called_once_with(['test@example.com'], '[UPDATE] News', 'Update body')

    def test_send_html_email(self, email_handler):
        """Test sending HTML email"""
        with patch('src.handlers.email_handler.smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_server)
            mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

            result = email_handler.send_email(
                to='recipient@example.com',
                subject='HTML Test',
                body='<h1>Hello</h1>',
                html=True,
            )

            assert result is True
            # Verify the message was sent
            mock_server.sendmail.assert_called_once()
