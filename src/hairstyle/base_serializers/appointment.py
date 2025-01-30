from rest_framework import serializers
from hairstyle.models.appointment import Appointment, Review, Message, ReviewImage


class AppointmentBaseSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(read_only=True)
    customer_id = serializers.IntegerField(write_only=True)
    service_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"


class ReviewBaseSerializer(serializers.ModelSerializer):
    appointment_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class ReviewImageBaseSerializer(serializers.ModelSerializer):
    review_id = serializers.IntegerField(write_only=True)
    image_id = serializers.IntegerField(write_only=True)
    order = serializers.IntegerField(read_only=True)

    class Meta:
        model = ReviewImage
        fields = "__all__"
