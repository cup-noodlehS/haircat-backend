from .base_serializers import (
    UserBaseSerializer,
    CustomerBaseSerializer,
    SpecialistBaseSerializer,
    DayAvailabilityBaseSerializer,
    DayOffBaseSerializer,
    BarberShopBaseSerializer,
    BarberShopImageBaseSerializer,
    BarberBaseSerializer,
    AppointmentTimeSlotBaseSerializer,
    QnaAnswerBaseSerializer,
    QnaQuestionBaseSerializer
)
from general.base_serializers import FileBaseSerializer, LocationBaseSerializer


class BarberSerializer(BarberBaseSerializer):
    pfp = FileBaseSerializer(read_only=True)
    barber_shop = BarberShopBaseSerializer(read_only=True)


class BarberShopImageSimpleSerializer(BarberShopImageBaseSerializer):
    image = FileBaseSerializer(read_only=True)


class BarberShopImageSerializer(BarberShopImageBaseSerializer):
    image = FileBaseSerializer(read_only=True)
    barber_shop = BarberShopBaseSerializer(read_only=True)


class SpecialistSimpleSerializer(SpecialistBaseSerializer):
    barber_shop = BarberShopBaseSerializer(read_only=True)


class UserSerializer(UserBaseSerializer):
    pfp = FileBaseSerializer(read_only=True)
    location = LocationBaseSerializer(read_only=True)
    specialist = SpecialistSimpleSerializer(read_only=True)
    customer = CustomerBaseSerializer(read_only=True)

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + (
            "pfp",
            "location",
            "specialist",
            "customer",
        )


class CustomerSerializer(CustomerBaseSerializer):
    user = UserSerializer(read_only=True)


class SpecialistSerializer(SpecialistBaseSerializer):
    user = UserSerializer(read_only=True)
    barber_shop = BarberShopBaseSerializer(read_only=True)


class DayAvailabilitySerializer(DayAvailabilityBaseSerializer):
    specialist = SpecialistSerializer(read_only=True)


class DayOffSerializer(DayOffBaseSerializer):
    specialist = SpecialistSerializer(read_only=True)


class BarberShopSerializer(BarberShopBaseSerializer):
    images = BarberShopImageSimpleSerializer(read_only=True, many=True)


class AppointmentTimeSlotSerializer(AppointmentTimeSlotBaseSerializer):
    day_availability = DayAvailabilitySerializer(read_only=True)


class QnaQuestionSerializer(QnaQuestionBaseSerializer):
    user = UserSerializer(read_only=True)


class QnaAnswerSerializer(QnaAnswerBaseSerializer):
    question = QnaQuestionBaseSerializer(read_only=True)
