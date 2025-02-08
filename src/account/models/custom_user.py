from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator

from general.models import File, Location


class CustomUser(AbstractUser):
    """
    **Required Fields:**
    - first_name: CharField to store the first name of the user.
    - last_name: CharField to store the last name of the user.
    - password: CharField to store the password of the user.
    - email: EmailField to store the email address of the user.
    - username: CharField to store the username of the user.
    - date_joined: Datetime field
    - phone_number: Text field
    - location: FK to Location
    - pfp: FK to File
    """

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
    )
    location = models.ForeignKey(
        Location, null=True, blank=True, on_delete=models.SET_NULL
    )
    pfp = models.ForeignKey(File, null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def pfp_url(self):
        if self.pfp:
            return self.pfp.url
        return None
    
    @property
    def is_barber_shop(self):
        specialist = getattr(self, "specialist", None)
        if specialist:
            return specialist.barber_shop is not None
        return False

    @property
    def is_specialist(self):
        specialist = getattr(self, "specialist", None)
        if specialist:
            return specialist.barber_shop is None
        return False

    @property
    def is_customer(self):
        """Check if user is a customer"""
        return hasattr(self, "customer")

    @property
    def specialist(self):
        """Get specialist profile"""
        return self.specialist

    @property
    def customer(self):
        """Get customer profile"""
        return self.customer

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
