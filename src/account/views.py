from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

from haircat.permissions import IsAuthenticated
from haircat.utils import GenericView

from .base_serializers import CustomTokenObtainPairSerializer, UserBaseSerializer
from .serializers import (
    UserSerializer,
    CustomerSerializer,
    SpecialistSerializer,
    DayAvailabilitySerializer,
    DayOffSerializer,
    BarberShopSerializer,
    BarberShopImageSerializer,
)
from .models import (
    CustomUser,
    Customer,
    Specialist,
    DayAvailability,
    DayOff,
    BarberShop,
    BarberShopImage,
)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserBaseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data["password"])
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Perform any logout actions if needed
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )


class UserView(GenericView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class CustomerView(GenericView):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class SpecialistView(GenericView):
    permission_classes = [IsAuthenticated]
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer


class DayAvailabilityView(GenericView):
    permission_classes = [IsAuthenticated]
    queryset = DayAvailability.objects.all()
    serializer_class = DayAvailabilitySerializer


class DayOffView(GenericView):
    permission_classes = [IsAuthenticated]
    queryset = DayOff.objects.all()
    serializer_class = DayOffSerializer


class BarberShopView(GenericView):
    permission_classes = [IsAuthenticated]
    queryset = BarberShop.objects.all()
    serializer_class = BarberShopSerializer


class BarberShopImageView(GenericView):
    permission_classes = [IsAuthenticated]
    queryset = BarberShopImage.objects.all()
    serializer_class = BarberShopImageSerializer
    allowed_methods = ["list", "retrieve", "create", "delete"]
