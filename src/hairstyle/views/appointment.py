from hairstyle.serializers.appointment import (
    AppointmentSerializer,
    ReviewImageSerializer,
    ReviewSerializer,
    MessageSerializer,
)
from hairstyle.models.appointment import Appointment, Review, ReviewImage, Message
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


class MessageView(GenericView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    allowed_methods = ["list", "create", "delete"]
