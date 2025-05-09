from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.apps import apps

from account.models import Customer
from hairstyle.models.service import Service
from general.models import File
from account.models import Barber


User = get_user_model()


def get_default_unread_messages():
    return {
        "specialist": 0,
        "customer": 0,
    }


class Appointment(models.Model):
    PENDING = 0
    CONFIRMED = 1
    COMPLETED = 2
    CANCELLED = 3

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="Appointments"
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="Appointments"
    )
    schedule = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    notes = models.TextField(max_length=255, null=True, blank=True)
    barber = models.ForeignKey(
        Barber,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="Appointments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def specialist(self):
        return self.service.specialist

    @property
    def status_display(self):
        return dict(self.STATUS_CHOICES)[self.status]

    def __str__(self):
        return f"{self.customer.user.full_name} - {self.service.name}"

    def save(self, *args, **kwargs):
        specialist = self.service.specialist

        # Fetch Appointments of that user that matches the schedule. If there is, throw an error
        if not specialist.barber_shop:
            if Appointment.objects.filter(
                service__specialist=specialist,
                schedule=self.schedule,
                status=self.CONFIRMED,
            ).exists():
                raise ValidationError("This time slot is already booked")
        else:
            if Appointment.objects.filter(
                service__specialist=specialist,
                barber=self.barber,
                schedule=self.schedule,
                status=self.CONFIRMED,
            ).exists():
                raise ValidationError("This time slot is already booked")

        if specialist.auto_accept_appointment and self.status == self.PENDING:
            self.status = self.CONFIRMED

        if not AppointmentMessageThread.objects.filter(appointment=self).exists():
            AppointmentMessageThread.objects.create(appointment=self)

        super().save(*args, **kwargs)


class Review(models.Model):

    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, related_name="Reviews"
    )
    rating = models.IntegerField(
        default=5, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def images(self):
        return self.Images.all().order_by("order")

    def __str__(self):
        return f"{self.appointment.customer.user.full_name} - {self.appointment.service.name}"


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="Images")
    image = models.ForeignKey(
        File, on_delete=models.CASCADE, related_name="ReviewImages"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.order = self.review.images.count()
        super().save(*args, **kwargs)


class AppointmentMessageThread(models.Model):
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE, related_name="message_thread"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.appointment.customer.user.full_name} - {self.appointment.service.name}"

    @property
    def last_message(self):
        return self.Messages.last()

    def get_formatted_last_message(self, user):
        if self.last_message.sender == user:
            return f"You: {self.last_message.message}"
        else:
            return f"{self.last_message.sender.full_name}: {self.last_message.message}"

    def mark_unread_messages(self, user):
        self.Messages.exclude(sender=user).update(read=True)

    def send_message(self, message, sender):
        # mark messages from other user as read then create new message
        self.mark_unread_messages(sender)
        return apps.get_model("hairstyle.AppointmentMessage").objects.create(
            appointment_message_thread=self, message=message, sender=sender
        )

    def get_messages(self, user):
        self.mark_unread_messages(user)
        return self.Messages.all()

    def get_unread_messages_count(self, user):
        return self.Messages.exclude(sender=user).filter(read=False).count()

    def get_title(self, user):
        if user == self.appointment.customer.user:
            return f"{self.appointment.service.specialist.user.full_name} - {self.appointment.service.name}"
        else:
            return f"{self.appointment.customer.user.full_name} - {self.appointment.service.name}"
    
    def get_title_pfp_url(self, user):
        if user == self.appointment.customer.user:
            return self.appointment.service.specialist.user.pfp.url
        else:
            return self.appointment.customer.user.pfp.url


class AppointmentMessage(models.Model):
    appointment_message_thread = models.ForeignKey(
        AppointmentMessageThread, on_delete=models.CASCADE, related_name="Messages"
    )
    message = models.TextField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Messages")
    schedule_change_req = models.DateTimeField(null=True, blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.appointment_message_thread.appointment.customer.user.full_name} - {self.appointment_message_thread.appointment.service.name}"
