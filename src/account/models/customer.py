from django.db import models

from .custom_user import CustomUser


class Customer(models.Model):
    """
    **Fields**
    - user: FK to CustomUser
    """

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="customer"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_points(self):
        """Get total reward points for customer"""
        return self.reward_points.aggregate(total=models.Sum("points"))["total"] or 0

    def __str__(self):
        return f"Customer - {self.user.full_name}"
