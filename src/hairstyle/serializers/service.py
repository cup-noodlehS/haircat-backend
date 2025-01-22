from hairstyle.base_serializers.service import ServiceBaseSerializer, LabelBaseSerializer
from account.base_serializers import SpecialistBaseSerializer, UserBaseSerializer
from general.base_serializers import FileBaseSerializer

class SpecialistSerializer(SpecialistBaseSerializer):
    user = UserBaseSerializer(read_only=True)


class ServiceSerializer(ServiceBaseSerializer):
    specialist = SpecialistSerializer(read_only=True)
    images = FileBaseSerializer(read_only=True, many=True)
    labels = LabelBaseSerializer(read_only=True, many=True)
