from django.db.models.signals import post_save
from django.dispatch import receiver
from general.webhooks import send_webhook
from .models.custom_user import UserNotification


@receiver(post_save, sender=UserNotification)
def notification_webhook_handler(sender, instance, created, **kwargs):
    """
    Send webhook notification when a new user notification is created.
    """
    if created:
        send_webhook(
            event_name='new_notif',
            user_id=instance.user.id,
            data={
                'id': instance.id,
                'message': instance.message,
                'is_read': instance.is_read,
                'created_at': instance.created_at.isoformat()
            }
        ) 