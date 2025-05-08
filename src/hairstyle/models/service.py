from django.db import models
from django.db.models import Avg

from account.models import Specialist
from general.models import File


class Label(models.Model):
    name = models.TextField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def total_services(self):
        return self.ServiceLabels.count()


class Service(models.Model):
    specialist = models.ForeignKey(
        Specialist, on_delete=models.CASCADE, related_name="Services"
    )
    name = models.TextField(max_length=50)
    description = models.TextField(max_length=255)
    duration_minutes = models.IntegerField(default=0)
    price = models.FloatField()
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def average_rating(self):
        from hairstyle.models.appointment import Review
        return Review.objects.filter(appointment__service=self).aggregate(Avg("rating"))["rating__avg"] or 0

    @property
    def total_reviews(self):
        from hairstyle.models.appointment import Review
        return Review.objects.filter(appointment__service=self).count()

    @property
    def total_appointments(self):
        return self.Appointments.count()

    @property
    def specialist_location(self):
        return self.specialist.location

    @property
    def images(self):
        return self.ServiceImages.all().order_by("order")

    @property
    def labels(self):
        return self.ServiceLabels.all()

    def __str__(self):
        user = self.specialist.user.full_name
        if self.specialist.barber_shop:
            user = self.specialist.barber_shop.name
        return f"{user} - {self.name}"


class ServiceLabel(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="ServiceLabels"
    )
    label = models.ForeignKey(
        Label, on_delete=models.CASCADE, related_name="ServiceLabels"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} - {self.label.name}"


class ServiceImage(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="ServiceImages"
    )
    image = models.ForeignKey(
        File, on_delete=models.CASCADE, related_name="ServiceImages"
    )
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} - {self.image.name}"

    def save(self, *args, **kwargs):
        self.order = self.service.images.count()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order"]
