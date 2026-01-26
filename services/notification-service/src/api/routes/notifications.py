from fastapi import APIRouter, Depends, HTTPException, status

from src.api.auth import verify_api_key
from src.db.session import SessionDep
import src.handlers.database_handler as crud
from src.handlers.email_handler import email_handler
from src.exceptions.database_exceptions import DatabaseError
import src.schemas.notification as schemas

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.post('/send', response_model=schemas.NotificationResponse)
def send_notification(db: SessionDep, request: schemas.NotificationRequest):
    """
    Send a notification to users based on their preferences.

    If recipient_names is provided, only those users will receive the notification
    (filtered by their preference settings). Otherwise, all users with the matching
    preference enabled will receive the notification.

    Args:
        db (SessionDep): Database session dependency
        request (schemas.NotificationRequest): Notification details

    Returns:
        schemas.NotificationResponse: Results of the notification send operation
    """
    try:
        if request.recipient_names:
            users = crud.get_entries_by_names(db=db, names=request.recipient_names)
            if request.notification_type == 'alert':
                users = [u for u in users if u.receive_alerts]
            else:
                users = [u for u in users if u.receive_updates]
        else:
            if request.notification_type == 'alert':
                users = crud.get_entries_by_preference(db=db, receive_alerts=True)
            else:
                users = crud.get_entries_by_preference(db=db, receive_updates=True)

        if not users:
            return schemas.NotificationResponse(
                total_recipients=0,
                successful=0,
                failed=0,
                results=[],
            )

        # Send notifications
        recipients = [user.email for user in users]

        if request.notification_type == 'alert':
            results = email_handler.send_alert(recipients, request.subject, request.body, html=request.html)
        else:
            results = email_handler.send_update(recipients, request.subject, request.body, html=request.html)

        result_list = [
            schemas.NotificationRecipientResult(email=email, success=success) for email, success in results.items()
        ]
        successful = sum(1 for r in result_list if r.success)

        return schemas.NotificationResponse(
            total_recipients=len(result_list),
            successful=successful,
            failed=len(result_list) - successful,
            results=result_list,
        )

    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Database error: {e}',
        )
