from haircat.utils import GenericView
from rest_framework.permissions import IsAuthenticated

from hairstyle.serializers.service import (
    ServiceSerializer,
    ServiceLabelSerializer,
    ServiceImageSerializer,
)
from hairstyle.base_serializers.service import LabelBaseSerializer

from hairstyle.models.service import Service, ServiceLabel, ServiceImage, Label


class ServiceView(GenericView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    permission_classes = [IsAuthenticated]


class ServiceLabelView(GenericView):
    serializer_class = ServiceLabelSerializer
    queryset = ServiceLabel.objects.all()
    allowed_methods = ["list", "retrieve", "create", "delete"]
    permission_classes = [IsAuthenticated]


class ServiceImageView(GenericView):
    serializer_class = ServiceImageSerializer
    queryset = ServiceImage.objects.all()
    allowed_methods = ["list", "retrieve", "create", "delete"]
    permission_classes = [IsAuthenticated]


class LabelView(GenericView):
    serializer_class = LabelBaseSerializer
    queryset = Label.objects.all()
    allowed_methods = ["list", "retrieve", "create", "delete"]
    permission_classes = [IsAuthenticated]
