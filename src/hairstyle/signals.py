from django.db.models.signals import post_save
from django.dispatch import receiver
from .models.appointment import Appointment
from general.webhooks import send_webhook


@receiver(post_save, sender=Appointment)
def appointment_webhook_handler(sender, instance, created, **kwargs):
    """
    Send webhook notifications to specialist and customer when appointment is created or updated.
    """
    # Determine event type
    event_name = 'new_appointment' if created else 'update_appointment'
    
    # Send webhook to specialist
    specialist_user_id = instance.service.specialist.user.id
    send_webhook(
        event_name=event_name,
        user_id=specialist_user_id,
        data={
            'id': instance.id,
        }
    )
    
    # Send webhook to customer
    customer_user_id = instance.customer.user.id
    send_webhook(
        event_name=event_name,
        user_id=customer_user_id,
        data={
            'id': instance.id,
        }
    ) 