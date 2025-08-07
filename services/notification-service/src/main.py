import smtplib
import os
from email.mime.text import MIMEText
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from src.api.router import api_router
from src.logger import logger


def cstm_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title="Notification-Service",
    openapi_url="/api/openapi.json",
    generate_unique_id_function=cstm_generate_unique_id,
)

app.include_router(api_router, prefix="/api")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom exception handler to log all HTTPExceptions before returning the response"""
    logger.error(
        f"HTTP Exception: {exc.status_code} - {exc.detail} for url: {request.url}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )



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
