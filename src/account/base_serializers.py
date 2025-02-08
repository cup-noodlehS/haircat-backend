from rest_framework import serializers
from account.models import (
    CustomUser,
    Customer,
    Specialist,
    DayAvailability,
    DayOff,
    BarberShop,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class BarberShopBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarberShop
        fields = "__all__"


class CustomerBaseSerializer(serializers.ModelSerializer):
    total_points = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Customer
        fields = "__all__"


class SpecialistBaseSerializer(serializers.ModelSerializer):
    is_available = serializers.BooleanField(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    barber_shop_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Specialist
        fields = "__all__"


class UserBaseSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    is_specialist = serializers.BooleanField(read_only=True)
    is_customer = serializers.BooleanField(read_only=True)
    is_barber_shop = serializers.BooleanField(read_only=True)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
            "date_joined",
            "phone_number",
            "full_name",
            "pfp_url",
            "is_specialist",
            "is_barber_shop",
            "is_customer",
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        if "@" in attrs["username"]:
            username = CustomUser.objects.get(email=attrs["username"]).username
            attrs["username"] = username
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = UserBaseSerializer(self.user).data
        return data


class DayAvailabilityBaseSerializer(serializers.ModelSerializer):
    specialist_id = serializers.IntegerField(write_only=True)
    day_of_week_display = serializers.CharField(read_only=True)

    class Meta:
        model = DayAvailability
        fields = "__all__"


class DayOffBaseSerializer(serializers.ModelSerializer):
    specialist_id = serializers.IntegerField(write_only=True)
    type_display = serializers.CharField(read_only=True)

    class Meta:
        model = DayOff
        fields = "__all__"
