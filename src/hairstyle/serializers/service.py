from hairstyle.base_serializers.service import (
    ServiceBaseSerializer,
    LabelBaseSerializer,
    ServiceLabelBaseSerializer,
    ServiceImageBaseSerializer,
)
from account.base_serializers import SpecialistBaseSerializer, UserBaseSerializer
from general.base_serializers import FileBaseSerializer


class SpecialistSerializer(SpecialistBaseSerializer):
    user = UserBaseSerializer(read_only=True)


class ServiceLabelSimpleSerializer(ServiceLabelBaseSerializer):
    label = LabelBaseSerializer(read_only=True)


class ServiceImageSimpleSerializer(ServiceImageBaseSerializer):
    image = FileBaseSerializer(read_only=True)


class ServiceSerializer(ServiceBaseSerializer):
    specialist = SpecialistSerializer(read_only=True)
    images = ServiceImageSimpleSerializer(read_only=True, many=True)
    labels = ServiceLabelSimpleSerializer(read_only=True, many=True)


class ServiceLabelSerializer(ServiceLabelBaseSerializer):
    service = ServiceBaseSerializer(read_only=True)
    label = LabelBaseSerializer(read_only=True)


class ServiceImageSerializer(ServiceImageBaseSerializer):
    service = ServiceBaseSerializer(read_only=True)
    image = FileBaseSerializer(read_only=True)
