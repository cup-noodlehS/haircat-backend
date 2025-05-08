from rest_framework import serializers
from hairstyle.models.appointment import AppointmentMessage, AppointmentMessageThread


class AppointmentMessageBaseSerializer(serializers.ModelSerializer):
    appointment_message_thread_id = serializers.IntegerField(write_only=True)
    sender_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = AppointmentMessage
        fields = '__all__'


class AppointmentMessageThreadBaseSerializer(serializers.ModelSerializer):
    appointment_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = AppointmentMessageThread
        fields = '__all__'