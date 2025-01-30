from hairstyle.serializers.appointment import AppointmentSerializer
from hairstyle.models.appointment import Appointment
from haircat.utils import GenericView


class AppointmentView(GenericView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
