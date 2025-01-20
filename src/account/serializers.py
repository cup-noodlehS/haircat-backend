from .base_serializers import UserBaseSerializer, CustomerBaseSerializer, SpecialistBaseSerializer
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
    user = UserSerializer()


class SpecialistSerializer(SpecialistBaseSerializer):
    user = UserSerializer()
