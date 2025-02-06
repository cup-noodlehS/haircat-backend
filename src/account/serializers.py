from .base_serializers import (
    UserBaseSerializer,
    CustomerBaseSerializer,
    SpecialistBaseSerializer,
    DayAvailabilityBaseSerializer,
    DayOffBaseSerializer,
)
from general.base_serializers import FileBaseSerializer, LocationBaseSerializer


class UserSerializer(UserBaseSerializer):
    pfp = FileBaseSerializer(read_only=True)
    location = LocationBaseSerializer(read_only=True)

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + (
            "pfp",
            "location",
        )


class CustomerSerializer(CustomerBaseSerializer):
    user = UserSerializer(read_only=True)


class SpecialistSerializer(SpecialistBaseSerializer):
    user = UserSerializer(read_only=True)


class DayAvailabilitySerializer(DayAvailabilityBaseSerializer):
    specialist = SpecialistSerializer(read_only=True)


class DayOffSerializer(DayOffBaseSerializer):
    specialist = SpecialistSerializer(read_only=True)
