from hairstyle.serializers.appointment import (
    AppointmentSerializer,
    ReviewImageSerializer,
    ReviewSerializer,
)
from hairstyle.models.appointment import Appointment, Review, ReviewImage
from haircat.utils import GenericView


class AppointmentView(GenericView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()


class ReviewView(GenericView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class ReviewImageView(GenericView):
    serializer_class = ReviewImageSerializer
    queryset = ReviewImage.objects.all()
    allowed_methods = ["list", "create", "delete"]

