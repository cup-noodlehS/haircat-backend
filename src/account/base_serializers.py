from rest_framework import serializers
from account.models import CustomUser


class UserBaseSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
            'date_joined',
            'phone_number'
        )
