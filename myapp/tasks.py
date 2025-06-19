# chat/tasks.py
from celery import shared_task
from .models import Message

@shared_task
def delete_all_messages():
    Message.objects.all().delete()
