from rest_framework import serializers
from hairstyle.models.appointment import AppointmentMessageThread, AppointmentMessage
from hairstyle.base_serializers.appointment_message import (
    AppointmentMessageBaseSerializer,
    AppointmentMessageThreadBaseSerializer,
)
from account.base_serializers import UserBaseSerializer
from hairstyle.base_serializers.appointment import AppointmentBaseSerializer


class AppointmentMessageSerializer(AppointmentMessageBaseSerializer):
    appointment_message_thread = AppointmentMessageThreadBaseSerializer(read_only=True)
    sender = UserBaseSerializer(read_only=True)


class ThreadLastMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = AppointmentMessage
        fields = ["id", "message", "sender", "sender_name", "created_at"]

    def get_sender_name(self, obj):
        return obj.sender.full_name


class AppointmentMessageThreadSerializer(AppointmentMessageThreadBaseSerializer):
    appointment = AppointmentBaseSerializer(read_only=True)
    last_message = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    unread_count = serializers.SerializerMethodField(read_only=True)
    formatted_last_message = serializers.SerializerMethodField(read_only=True)

    def get_last_message(self, obj):
        if not obj.last_message:
            return None
        return ThreadLastMessageSerializer(obj.last_message).data

    def get_title(self, obj):
        request = self.context.get("request")
        if not request:
            return str(obj)
        return obj.get_title(request.user)

    def get_unread_count(self, obj):
        request = self.context.get("request")
        if not request:
            return 0
        return obj.get_unread_messages_count(request.user)

    def get_formatted_last_message(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        return obj.get_formatted_last_message(request.user)
