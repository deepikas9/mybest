# myapp/management/commands/delete_messages.py
import os
import django
from django.core.management.base import BaseCommand
from myapp.models import ChatMessage

class Command(BaseCommand):
    help = 'Deletes all messages from the database'

    def handle(self, *args, **kwargs):
        # Set up Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ume.settings')
        django.setup()

        # Delete all messages
        ChatMessage.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all messages'))
