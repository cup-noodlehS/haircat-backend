from hairstyle.base_serializers import AppointmentBaseSerializer, ServiceBaseSerializer
from account.base_serializers import SpecialistBaseSerializer, CustomerBaseSerializer, UserBaseSerializer
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

class AppointmentSerializer(AppointmentBaseSerializer):
    customer = CustomerSerializer(read_only=True)
    specialist = SpecialistSerializer(read_only=True)
    service = ServiceBaseSerializer(read_only=True)

