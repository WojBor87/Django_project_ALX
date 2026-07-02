from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from devboard.models import Task
from devboard.tasks import send_overdue_digest


def save_done_info(sender, instance, **kwargs):
    print(f"Zapisano  {instance} do bazy!")


@receiver(post_save, sender=Task, dispatch_uid='save_done_info2_on_tasks')
def save_done_info2(sender, instance, **kwargs):
    print(f"Zapisano  {instance} do bazy!")
    send_overdue_digest.delay()


@receiver(pre_save, sender=Task, dispatch_uid="check_old_status_check")
def check_old_status(sender, instance, **kwargs):
    if instance.pk:
        status = sender.objects.filter(pk=instance.pk).first().status
        instance._old_status = status


@receiver(post_save, sender=Task, dispatch_uid="log_status_change_log")
def log_status_change(sender, instance, created, **kwargs):
    if created:
        return
    if hasattr(instance, "_old_status") and (instance._old_status != instance.status):
        print(f"Task {instance.title} status changed: {instance._old_status} -> {instance.status}")