from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models.appointment import Appointment
from general.webhooks import send_webhook
from account.models.custom_user import UserNotification


@receiver(pre_save, sender=Appointment)
def appointment_status_change_handler(sender, instance, **kwargs):
    """
    Create user notification when appointment status changes to confirmed.
    """
    if not instance.pk:  # Skip for new instances
        return
        
    try:
        old_instance = Appointment.objects.get(pk=instance.pk)
        if old_instance.status != Appointment.CONFIRMED and instance.status == Appointment.CONFIRMED:
            UserNotification.objects.create(
                user=instance.customer.user,
                message=f"Your appointment for {instance.service.name} has been confirmed"
            )
    except Appointment.DoesNotExist:
        pass


@receiver(post_save, sender=Appointment)
def appointment_webhook_handler(sender, instance, created, **kwargs):
    """
    Send webhook notifications to specialist and customer when appointment is created or updated.
    Also create user notification for specialist when there is a new appointment.
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

    # Create notification for specialist if it's a new appointment
    if created:
        UserNotification.objects.create(
            user=instance.service.specialist.user,
            message=f"New appointment request from {instance.customer.user.full_name} for {instance.service.name}"
        ) 