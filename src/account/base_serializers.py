from rest_framework import serializers
from account.models import (
    CustomUser,
    Customer,
    Specialist,
    DayAvailability,
    DayOff,
    BarberShop,
    BarberShopImage,
    SpecialistShopImage,
    Barber,
    AppointmentTimeSlot,
    QnaAnswer,
    QnaQuestion,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class BarberBaseSerializer(serializers.ModelSerializer):
    pfp_id = serializers.IntegerField(write_only=True, required=False)
    barber_shop_id = serializers.IntegerField(write_only=True)
    average_rating = serializers.FloatField(read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Barber
        fields = "__all__"


class BarberShopBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarberShop
        fields = "__all__"


class BarberShopImageBaseSerializer(serializers.ModelSerializer):
    barber_shop_id = serializers.IntegerField(write_only=True)
    image_id = serializers.IntegerField(write_only=True)
    order = serializers.IntegerField(read_only=True)

    class Meta:
        model = BarberShopImage
        fields = "__all__"


class CustomerBaseSerializer(serializers.ModelSerializer):
    total_points = serializers.IntegerField(read_only=True)
    has_active_appointment = serializers.BooleanField(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Customer
        fields = "__all__"


class SpecialistBaseSerializer(serializers.ModelSerializer):
    is_available = serializers.BooleanField(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    barber_shop_id = serializers.IntegerField(write_only=True, required=False)
    average_rating = serializers.FloatField(read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Specialist
        fields = "__all__"


class UserBaseSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    is_specialist = serializers.BooleanField(read_only=True)
    is_customer = serializers.BooleanField(read_only=True)
    is_barber_shop = serializers.BooleanField(read_only=True)
    pfp_id = serializers.IntegerField(write_only=True, required=False)

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
            "pfp_id",
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


class AppointmentTimeSlotBaseSerializer(serializers.ModelSerializer):
    day_availability_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = AppointmentTimeSlot
        fields = "__all__"


class QnaQuestionBaseSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    specialist_id = serializers.IntegerField(write_only=True)
    answer_message = serializers.CharField(read_only=True)

    class Meta:
        model = QnaQuestion
        fields = "__all__"


class QnaAnswerBaseSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = QnaAnswer
        fields = "__all__"


class SpecialistShopImageBaseSerializer(serializers.ModelSerializer):
    specialist_id = serializers.IntegerField(write_only=True)
    image_id = serializers.IntegerField(write_only=True)
    order = serializers.IntegerField(read_only=True)

    class Meta:
        model = SpecialistShopImage
        fields = "__all__"