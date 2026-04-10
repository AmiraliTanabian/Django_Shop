import os.path
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import ticket_attachment


@shared_task
def cleanup_orphaned_files():
    print("Task runned!")
    limit = timezone.now() - timedelta(seconds=10)
    orphaned_files = ticket_attachment.objects.filter(ticket=None, created_time__lt=limit)

    for file in orphaned_files:
        try:
            if os.path.exists(file.files.path):
                os.remove(file.files.path)
            file.delete()

        except Exception as Error:
            print(Error)
            print("---------------------")
            print("Error cleaning up file with path : {}".format(file.files.path))

    print("Clean up finished!")
    return "Clean up finished!"
