from django.db import models
from django.db.models import Avg

from account.models import Specialist
from general.models import File


class Label(models.Model):
    name = models.TextField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


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
        return self.appointments.reviews.aggregate(Avg("rating"))["rating__avg"] or 0

    @property
    def total_reviews(self):
        return self.appointments.reviews.count()

    @property
    def total_appointments(self):
        return self.appointments.count()

    @property
    def specialist_location(self):
        return self.specialist.location
    
    @property
    def images(self):
        return self.ServiceImages.all()
    
    @property
    def labels(self):
        return self.ServiceLabels.all()

    def __str__(self):
        return self.name


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
