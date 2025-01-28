from rest_framework import serializers
from hairstyle.models.appointment import Appointment, Review, Message


class AppointmentBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"
