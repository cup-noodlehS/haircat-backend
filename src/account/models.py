from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator, MinValueValidator

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
    def is_specialist(self):
        """Check if user is a specialist"""
        return hasattr(self, "specialist")

    @property
    def is_customer(self):
        """Check if user is a customer"""
        return hasattr(self, "customer")

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


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


class Specialist(models.Model):
    """
    **Fields**
    - user: FK to CustomUser
    - bio: text field
    - point_to_php: float field
    """

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="specialist"
    )
    bio = models.TextField(
        blank=True, null=True, help_text="Specialist's biography and description"
    )
    point_to_php = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text="Conversion rate from points to PHP currency",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_available(self, date, time):
        """Check if specialist is available at given date/time"""
        # Skip if day off
        if self.days_off.filter(date=date).exists():
            return False

        # Check regular availability
        weekday = date.weekday()
        return self.availabilities.filter(
            day_of_week=weekday, start_time__lte=time, end_time__gt=time
        ).exists()

    def __str__(self):
        return f"Specialist - {self.user.full_name}"


class RewardPoints(models.Model):
    """
    Tracks reward points earned by customers from specialists.

    **Fields**
    - customer: FK to Customer who earned the points
    - specialist: FK to Specialist who awarded the points
    - points: Integer amount of points awarded
    - created_at: Timestamp when points were awarded
    """

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="reward_points",
        help_text="Customer who earned these points",
    )
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        related_name="awarded_points",
        help_text="Specialist who awarded these points",
    )
    points = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of points awarded (minimum 1)",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Reward Points"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.points} points from {self.specialist} to {self.customer}"


class DayAvailability(models.Model):
    """
    Represents a specialist's availability for a specific day of the week.

    **Fields**
    - specialist: FK to Specialist this availability belongs to
    - day_of_week: Integer representing day of week (0=Sunday through 6=Saturday)
    - start_time: Time when specialist starts being available
    - end_time: Time when specialist stops being available

    **Properties**
    - day_of_week_display: Returns string name of day (e.g. "Monday")
    """

    # Day of week constants
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6

    DAY_CHOICES = [
        (SUNDAY, "Sunday"),
        (MONDAY, "Monday"),
        (TUESDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday"),
        (SATURDAY, "Saturday"),
    ]

    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        related_name="availabilities",
        help_text="The specialist this availability belongs to",
    )
    day_of_week = models.IntegerField(
        choices=DAY_CHOICES, help_text="Day of week (0=Sunday through 6=Saturday)"
    )
    start_time = models.TimeField(
        help_text="Time when specialist starts being available"
    )
    end_time = models.TimeField(help_text="Time when specialist stops being available")

    class Meta:
        verbose_name = "Day Availability"
        verbose_name_plural = "Day Availabilities"
        ordering = ["day_of_week", "start_time"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F("end_time")),
                name="start_time_before_end_time",
            )
        ]

    @property
    def day_of_week_display(self):
        """Returns the string representation of the day of week."""
        return dict(self.DAY_CHOICES)[self.day_of_week]

    def __str__(self):
        return f"{self.specialist}'s availability on {self.day_of_week_display}"


class DayOff(models.Model):
    """
    Represents a day off for a specialist.

    **Fields**
    - specialist: FK to Specialist this day off belongs to
    - type: IntegerField for type of day off (vacation, sick, personal, etc.)
    - date: Date of the day off
    - created_at: Timestamp when this record was created
    """

    HOLIDAY = 0
    VACATION = 1
    SICK = 2
    PERSONAL = 3
    OTHER = 4

    TYPE_CHOICES = [
        (HOLIDAY, "Holiday"),
        (VACATION, "Vacation"),
        (SICK, "Sick Leave"),
        (PERSONAL, "Personal"),
        (OTHER, "Other"),
    ]

    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        related_name="days_off",
        help_text="The specialist taking the day off",
    )
    type = models.IntegerField(choices=TYPE_CHOICES, help_text="Type of day off")
    date = models.DateField(help_text="Date of the day off")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When this day off was recorded"
    )

    @property
    def type_display(self):
        return dict(self.TYPE_CHOICES)[self.type]

    class Meta:
        verbose_name = "Day Off"
        verbose_name_plural = "Days Off"
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["specialist", "date"], name="unique_specialist_day_off"
            )
        ]

    def __str__(self):
        return f"{self.specialist}'s {self.type_display} day off on {self.date}"
