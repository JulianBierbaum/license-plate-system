import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.config import settings
from src.logger import logger
from src.exceptions.sending_exceptions import EmailSendError


class EmailHandler:
    """Handles sending emails via SMTP relay"""

    def __init__(
        self,
        smtp_host: str | None = None,
        smtp_port: int | None = None,
        sender_address: str | None = None,
    ):
        self.smtp_host = smtp_host or settings.smtp_relay_host
        self.smtp_port = smtp_port or settings.smtp_port
        self.sender_address = sender_address or settings.sender_address

    def send_email(self, to: str, subject: str, body: str, html: bool = False) -> bool:
        """Send a single email

        Args:
            to: recipient email address
            subject: email subject
            body: email body content
            html: if True, send as HTML email

        Returns:
            True if email was sent successfully

        Raises:
            EmailSendError: if sending fails
        """
        try:
            if html:
                msg = MIMEMultipart('alternative')
                msg.attach(MIMEText(body, 'html'))
            else:
                msg = MIMEText(body)

            msg['Subject'] = subject
            msg['From'] = self.sender_address
            msg['To'] = to

            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30) as smtp_server:
                smtp_server.sendmail(self.sender_address, [to], msg.as_string())

            logger.info(f'Email sent successfully to {to}')
            return True

        except smtplib.SMTPException as e:
            logger.error(f'SMTP error sending email to {to}: {e}')
            raise EmailSendError(f'Failed to send email: {e}') from e
        except Exception as e:
            logger.error(f'Unexpected error sending email to {to}: {e}')
            raise EmailSendError(f'Failed to send email: {e}') from e

    def send_bulk_email(self, recipients: list[str], subject: str, body: str, html: bool = False) -> dict[str, bool]:
        """Send email to multiple recipients

        Args:
            recipients: list of email addresses
            subject: email subject
            body: email body content
            html: if True, send as HTML email

        Returns:
            dict mapping email addresses to success status
        """
        results = {}
        for recipient in recipients:
            try:
                self.send_email(recipient, subject, body, html)
                results[recipient] = True
            except EmailSendError:
                results[recipient] = False

        return results

    def send_alert(self, recipients: list[str], subject: str, body: str, html: bool = False) -> dict[str, bool]:
        """Send alert notification to recipients

        Args:
            recipients: list of email addresses
            subject: alert subject
            body: alert body
            html: if True, send as HTML email

        Returns:
            dict mapping email addresses to success status
        """
        prefixed_subject = f'[ALERT] {subject}'
        return self.send_bulk_email(recipients, prefixed_subject, body, html=html)

    def send_update(self, recipients: list[str], subject: str, body: str, html: bool = False) -> dict[str, bool]:
        """Send update notification to recipients

        Args:
            recipients: list of email addresses
            subject: update subject
            body: update body
            html: if True, send as HTML email

        Returns:
            dict mapping email addresses to success status
        """
        prefixed_subject = f'[UPDATE] {subject}'
        return self.send_bulk_email(recipients, prefixed_subject, body, html=html)


# Default handler instance
email_handler = EmailHandler()
