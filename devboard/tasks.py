from celery import shared_task

from devboard.models import Task


@shared_task
def send_overdue_digest():
    overdue = Task.objects.overdue()
    content = f"Zadania z przkroczonym harmonogramem wykonania: {overdue}"
    print(content)
    return overdue.count()