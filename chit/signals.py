from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import *



@receiver(post_save, sender=User)
def log_user_creation(sender, instance, created, **kwargs):
    """Log user creation."""
    if created:
        UserActionLog.objects.create(user=instance, action='CREATED')


@receiver(pre_delete, sender=User)
def log_user_deletion(sender, instance, **kwargs):
    """Log user deletion."""
    UserActionLog.objects.create(user=instance, action='DELETED')
