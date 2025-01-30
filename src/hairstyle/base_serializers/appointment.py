from rest_framework import serializers
from hairstyle.models.appointment import Appointment, Review, Message


class AppointmentBaseSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(read_only=True)
    customer_id = serializers.IntegerField(write_only=True)
    service_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"
