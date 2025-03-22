from django.db import models
from django.core.validators import MinValueValidator

from .custom_user import CustomUser
from .customer import Customer
from general.models import File


class BarberShop(models.Model):
    """
    Represents a barber shop.
    """

    name = models.CharField(max_length=255, help_text="Name of the barber shop")

    @property
    def images(self):
        return self.images.all().order_by("order")

    def __str__(self):
        return self.name


class BarberShopImage(models.Model):
    barber_shop = models.ForeignKey(
        BarberShop, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ForeignKey(
        File, on_delete=models.CASCADE, related_name="barber_shop_images"
    )
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.barber_shop.name} - {self.image.name}"

    def save(self, *args, **kwargs):
        self.order = self.barber_shop.images.count()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order"]


class Barber(models.Model):
    barber_shop = models.ForeignKey(
        BarberShop, on_delete=models.CASCADE, related_name="barbers"
    )
    name = models.CharField(max_length=255, help_text="Name of the barber")
    info = models.TextField(
        blank=True, null=True, help_text="Information about the barber"
    )
    pfp = models.ForeignKey(
        File,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="barber_pfps",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def average_rating(self):
        reviews = self.Appointments.exclude(Reviews__isnull=True).values_list(
            "Reviews__rating", flat=True
        )
        if not reviews:
            return 0
        return round(sum(reviews) / len(reviews), 1)

    @property
    def reviews_count(self):
        return self.Appointments.exclude(Reviews__isnull=True).count()

    def __str__(self):
        return f"{self.barber_shop.name} - {self.name}"


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
    google_maps_link = models.URLField(
        blank=True,
        null=True,
        help_text="Google Maps link for the specialist's location",
    )
    barber_shop = models.OneToOneField(
        BarberShop,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="specialists",
        help_text="If user type is a barber shop",
    )
    auto_accept_appointment = models.BooleanField(
        default=False,
        help_text="If the specialist should automatically accept appointments",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def average_rating(self):
        from hairstyle.models.appointment import Review

        reviews = Review.objects.filter(
            appointment__service__specialist=self
        ).values_list("rating", flat=True)
        if not reviews:
            return 0
        return round(sum(reviews) / len(reviews), 1)

    @property
    def reviews_count(self):
        from hairstyle.models.appointment import Review

        return Review.objects.filter(appointment__service__specialist=self).count()

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

    def create_time_slots(self, slots_data):
        """
        Create multiple time slots for this day availability.
        
        Args:
            slots_data: List of dicts with start_time and end_time
        """
        from django.core.exceptions import ValidationError
        
        created_slots = []
        for slot_data in slots_data:
            try:
                slot = AppointmentTimeSlot(
                    day_availability=self,
                    start_time=slot_data['start_time'],
                    end_time=slot_data['end_time'],
                    is_available=slot_data.get('is_available', True)
                )
                slot.save()
                created_slots.append(slot)
            except ValidationError as e:
                # Roll back any created slots
                for created_slot in created_slots:
                    created_slot.delete()
                raise ValidationError(f"Invalid time slot: {e}")
        
        return created_slots


class AppointmentTimeSlot(models.Model):
    """
    Represents a specific time slot for appointments within a day's availability.

    **Fields**
    - day_availability: FK to DayAvailability this slot belongs to
    - start_time: Time when the appointment slot starts
    - end_time: Time when the appointment slot ends
    - is_available: Whether this time slot is available for booking
    - created_at: Timestamp when this slot was created
    """

    day_availability = models.ForeignKey(
        DayAvailability,
        on_delete=models.CASCADE,
        related_name="time_slots",
        help_text="The day availability this time slot belongs to",
    )
    start_time = models.TimeField(
        help_text="Time when the appointment slot starts"
    )
    end_time = models.TimeField(
        help_text="Time when the appointment slot ends"
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Whether this time slot is available for booking"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this time slot was created"
    )

    class Meta:
        verbose_name = "Appointment Time Slot"
        verbose_name_plural = "Appointment Time Slots"
        ordering = ["start_time"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F("end_time")),
                name="appointment_start_before_end",
            ),
            # Prevent overlapping time slots for the same day availability
            models.UniqueConstraint(
                fields=['day_availability', 'start_time', 'end_time'],
                name='unique_time_slot'
            )
        ]

    def __str__(self):
        return f"{self.day_availability}'s slot: {self.start_time}-{self.end_time}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Check if the time slot is within the day availability's time range
        if (self.start_time < self.day_availability.start_time or 
            self.end_time > self.day_availability.end_time):
            raise ValidationError(
                "Time slot must be within the day availability's time range"
            )
        
        # Check for overlapping slots
        overlapping = AppointmentTimeSlot.objects.filter(
            day_availability=self.day_availability,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )
        if self.pk:  # If updating existing slot
            overlapping = overlapping.exclude(pk=self.pk)
        
        if overlapping.exists():
            raise ValidationError(
                "This time slot overlaps with an existing slot"
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


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


class QnaQuestion(models.Model):
    message = models.TextField(max_length=100, help_text="Question message")
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="qna_questions"
    )
    specialist = models.ForeignKey(
        Specialist, on_delete=models.CASCADE, related_name="qna_questions"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def answer_message(self):
        return self.answer.message if hasattr(self, "answer") else ''

    def __str__(self):
        return f"{self.user} asked {self.specialist}: {self.message}"


class QnaAnswer(models.Model):
    message = models.TextField(max_length=100, help_text="Answer message")
    question = models.OneToOneField(
        QnaQuestion, on_delete=models.CASCADE, related_name="answer"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question.user} asked {self.question.specialist}: {self.message}"
