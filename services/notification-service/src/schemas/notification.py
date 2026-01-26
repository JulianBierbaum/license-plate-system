from typing import Literal

from pydantic import BaseModel, Field


class NotificationRequest(BaseModel):
    """Schema for sending a notification"""

    notification_type: Literal['alert', 'update'] = Field(..., description="Type of notification: 'alert' or 'update'")
    subject: str = Field(..., min_length=1, max_length=200, description='Email subject')
    body: str = Field(..., min_length=1, description='Email body content')
    recipient_names: list[str] | None = Field(
        default=None, description='Optional list of specific user names to send to.'
    )
    html: bool = Field(default=False, description='If true, send body as HTML')


class NotificationRecipientResult(BaseModel):
    """Result for a single recipient"""

    email: str
    success: bool


class NotificationResponse(BaseModel):
    """Response after sending notifications"""

    total_recipients: int
    successful: int
    failed: int
    results: list[NotificationRecipientResult]
