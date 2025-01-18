from django.db import models

class Location(models.Model):
    name = models.TextField(max_length=255)
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()

    def __str__(self):
        return f"{self.name} - ({self.x_coordinate}, {self.y_coordinate})"
