import smtplib
import os
from email.mime.text import MIMEText
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from src.api.router import api_router


def cstm_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title="Notification-Service",
    openapi_url="/api/openapi.json",
    generate_unique_id_function=cstm_generate_unique_id,
)

app.include_router(api_router, prefix="/api")


""" def main():
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
    print("Hello World!")
 """