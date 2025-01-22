from rest_framework import serializers
from hairstyle.models.service import Service, ServiceImage, ServiceLabel, Label


class ServiceBaseSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    total_reviews = serializers.IntegerField(read_only=True)
    total_appointments = serializers.IntegerField(read_only=True)
    specialist_location = serializers.CharField(read_only=True)
    specialist_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Service
        fields = "__all__"


class LabelBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"
