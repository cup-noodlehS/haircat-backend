from rest_framework import serializers
from general.models import Location

class LocationBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
