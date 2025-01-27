from general.models import File, Location
from general.base_serializers import FileBaseSerializer, LocationBaseSerializer
from haircat.utils import GenericView

class FileView(GenericView):
    serializer_class = FileBaseSerializer
    queryset = File.objects.all()

class LocationView(GenericView):
    serializer_class = LocationBaseSerializer
    queryset = Location.objects.all()
