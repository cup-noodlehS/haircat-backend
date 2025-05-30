from django.utils import timezone
from datetime import timedelta
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings

from .models.appointment import Appointment
from account.models.custom_user import UserNotification

def check_pending_appointments():
    """Check and update pending appointments that are past their schedule"""
    now = timezone.now()
    pending_appointments = Appointment.objects.filter(
        status=Appointment.PENDING,
        schedule__lt=now
    )
    
    for appointment in pending_appointments:
        appointment.status = Appointment.CANCELLED
        appointment.save()
        
        # Create notifications for both customer and specialist
        UserNotification.objects.create(
            user=appointment.customer.user,
            message=f"Your appointment for {appointment.service.name} has been automatically cancelled as it was not confirmed before the scheduled time."
        )
        UserNotification.objects.create(
            user=appointment.service.specialist.user,
            message=f"Appointment with {appointment.customer.user.full_name} for {appointment.service.name} has been automatically cancelled as it was not confirmed before the scheduled time."
        )

def notify_day_before():
    """Create notifications for appointments scheduled for tomorrow"""
    tomorrow = timezone.now() + timedelta(days=1)
    tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    upcoming_appointments = Appointment.objects.filter(
        schedule__range=(tomorrow_start, tomorrow_end),
        status__in=[Appointment.PENDING, Appointment.CONFIRMED]
    )
    
    for appointment in upcoming_appointments:
        UserNotification.objects.create(
            user=appointment.service.specialist.user,
            message=f"You have an appointment tomorrow with {appointment.customer.user.full_name} for {appointment.service.name} at {appointment.schedule.strftime('%I:%M %p')}"
        )

def notify_six_hours_before():
    """Create notifications for confirmed appointments 6 hours before schedule"""
    six_hours_from_now = timezone.now() + timedelta(hours=6)
    time_window_start = six_hours_from_now - timedelta(minutes=5)
    time_window_end = six_hours_from_now + timedelta(minutes=5)
    
    upcoming_appointments = Appointment.objects.filter(
        schedule__range=(time_window_start, time_window_end),
        status=Appointment.CONFIRMED
    )
    
    for appointment in upcoming_appointments:
        # Notify customer
        UserNotification.objects.create(
            user=appointment.customer.user,
            message=f"Reminder: Your appointment for {appointment.service.name} is in 6 hours at {appointment.schedule.strftime('%I:%M %p')}"
        )
        # Notify specialist
        UserNotification.objects.create(
            user=appointment.service.specialist.user,
            message=f"Reminder: You have an appointment with {appointment.customer.user.full_name} for {appointment.service.name} in 6 hours at {appointment.schedule.strftime('%I:%M %p')}"
        )

def check_completed_appointments():
    """Check and update confirmed appointments that are past their schedule"""
    now = timezone.now()
    past_appointments = Appointment.objects.filter(
        status=Appointment.CONFIRMED,
        schedule__lt=now
    )
    
    for appointment in past_appointments:
        appointment.status = Appointment.COMPLETED
        appointment.save()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    # Run every hour to check pending appointments
    scheduler.add_job(
        check_pending_appointments,
        CronTrigger(hour="*"),
        id="check_pending_appointments",
        replace_existing=True,
    )
    
    # Run at midnight to notify about next day's appointments
    scheduler.add_job(
        notify_day_before,
        CronTrigger(hour="0", minute="0"),
        id="notify_day_before",
        replace_existing=True,
    )
    
    # Run every 5 minutes to check for 6-hour notifications
    scheduler.add_job(
        notify_six_hours_before,
        CronTrigger(minute="*/5"),
        id="notify_six_hours_before",
        replace_existing=True,
    )
    
    # Run every hour to check completed appointments
    scheduler.add_job(
        check_completed_appointments,
        CronTrigger(hour="*"),
        id="check_completed_appointments",
        replace_existing=True,
    )
    
    scheduler.start() 