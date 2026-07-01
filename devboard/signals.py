from django.db.models.signals import post_save
from django.dispatch import receiver

from devboard.models import Task


def save_done_info(sender, instance, **kwargs):
    print(f"Zapisano  {instance} do bazy!")

@receiver(post_save, sender=Task, dispatch_uid='save_done_info2_on_tasks')
def save_done_info2(sender, instance, **kwargs):
    print(f"Zapisano  {instance} do bazy!")


