"""
ContentIQ - Celery Application Configuration
Configures Celery distributed task queue and Celery Beat periodic scheduler.
Note for Windows: Must run worker with `--pool=solo` parameter:
    celery -A app.core.celery_app worker --pool=solo -l info
"""
import os
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

# Initialize Celery app instance
celery_app = Celery(
    "contentiq",
    broker=os.getenv("REDIS_URL", settings.REDIS_URL),
    backend=os.getenv("REDIS_URL", settings.REDIS_URL),
    include=["app.tasks.scheduler"]
)

# Celery Configuration Settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=False,
    broker_connection_retry_on_startup=True,
    task_track_started=True,
)

# Celery Beat Schedule Configuration
celery_app.conf.beat_schedule = {
    # Task 1: Check and publish due posts every 30 seconds
    "publish-due-posts-every-30s": {
        "task": "app.tasks.scheduler.publish_due_posts_task",
        "schedule": 30.0,
    },
    # Task 2: Check for upcoming posts scheduled within next 24 hours every 15 minutes
    "check-upcoming-posts-every-15m": {
        "task": "app.tasks.scheduler.generate_upcoming_notifications_task",
        "schedule": crontab(minute="*/15"),
    },
}
