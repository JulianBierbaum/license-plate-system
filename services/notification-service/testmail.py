import smtplib
from email.mime.text import MIMEText

def main():
    subject = "Test Mail"
    body = "This is a test mail"
    sender = "notifications.license-plate-system@zotter.at"
    recipients = ["bierbaumjulian@gmail.com"]
    smtp_relay = "172.16.1.164" # zotter smtp open mail relay

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP(smtp_relay, 25) as smtp_server:
        smtp_server.sendmail(sender, recipients, msg.as_string())

    print("Message sent!")

if __name__ == "__main__":
    main()
