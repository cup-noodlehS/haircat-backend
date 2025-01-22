from haircat.utils import GenericView

from hairstyle.serializers.service import ServiceSerializer
from hairstyle.models.service import Service

class ServiceView(GenericView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
