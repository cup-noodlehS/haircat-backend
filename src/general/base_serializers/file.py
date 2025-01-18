from rest_framework import serializers
from general.models import File

class FileBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
