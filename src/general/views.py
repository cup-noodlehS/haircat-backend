from general.models import File, Location
from general.base_serializers import FileBaseSerializer, LocationBaseSerializer
from haircat.utils import GenericView
from rest_framework.permissions import AllowAny


class FileView(GenericView):
    serializer_class = FileBaseSerializer
    queryset = File.objects.all()
    permission_classes = [AllowAny]  # Allow unauthenticated access for file uploads


class LocationView(GenericView):
    serializer_class = LocationBaseSerializer
    queryset = Location.objects.all()
