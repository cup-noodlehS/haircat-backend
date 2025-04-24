from django.db import models
from django.utils import timezone

from .custom_user import CustomUser

class Customer(models.Model):
    """
    **Fields**
    - user: FK to CustomUser
    """

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="customer"
    )
    favorite_specialists = models.ManyToManyField(
        'account.Specialist', 
        related_name='favorited_by', 
        blank=True,
        help_text="Specialists marked as favorite by this customer"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_points(self):
        """Get total reward points for customer"""
        return self.reward_points.aggregate(total=models.Sum("points"))["total"] or 0

    @property
    def has_active_appointment(self):
        # Import inside method to avoid circular import
        from hairstyle.models.appointment import Appointment
        return self.Appointments.filter(schedule__gte=timezone.now(), status__in=[Appointment.CONFIRMED, Appointment.PENDING]).exists()

    def __str__(self):
        return f"Customer - {self.user.full_name}"
