from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from account.models import Customer
from hairstyle.models.service import Service
from general.models import File
from account.models import Barber


User = get_user_model()

def get_default_unread_messages():
    return {
        'specialist': 0,
        'customer': 0,
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
    unread_messages = models.JSONField(default=get_default_unread_messages)
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
        if specialist.auto_accept_appointment and self.status == self.PENDING:
            self.status = self.CONFIRMED
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


class Message(models.Model):
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, related_name="Messages"
    )
    message = models.TextField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Messages")
    schedule_change_req = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.appointment.customer.user.full_name} - {self.appointment.service.name}"
