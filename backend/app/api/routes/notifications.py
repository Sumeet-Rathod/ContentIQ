from fastapi import APIRouter, Depends, Query
from typing import List
from app.schemas.feedback import NotificationResponse
from app.services.notification_service import (
    list_notifications, mark_notification_read, mark_all_notifications_read
)
from app.core.deps import get_current_user

router = APIRouter(prefix="/notifications", tags=["M6: In-App Notifications"])

@router.get("", response_model=List[NotificationResponse])
async def get_notifications(
    unread_only: bool = Query(False),
    current_user: dict = Depends(get_current_user)
):
    """Retrieve in-app notifications for the caller's tenant."""
    return await list_notifications(current_user["tenant_id"], unread_only=unread_only)

@router.put("/{notification_id}/read")
async def mark_read(
    notification_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Mark an individual notification as read."""
    return await mark_notification_read(current_user["tenant_id"], notification_id)

@router.put("/read-all")
async def mark_all_read(current_user: dict = Depends(get_current_user)):
    """Mark all unread notifications for tenant as read."""
    return await mark_all_notifications_read(current_user["tenant_id"])
