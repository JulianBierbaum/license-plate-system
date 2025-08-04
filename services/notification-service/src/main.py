import smtplib
import os
from email.mime.text import MIMEText


def main():
    subject = "Test Mail"
    body = "This is a test mail"
    sender = os.getenv("SENDER_ADDRESS", "")
    recipients = ["bierbaumjulian@gmail.com"]
    password = os.getenv("APP_PASSWORD", "")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


if __name__ == "__main__":
    main()
