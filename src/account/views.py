from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated as DRFIsAuthenticated
from django.shortcuts import get_object_or_404

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
    BarberSerializer,
    AppointmentTimeSlotSerializer,
    QnaAnswerSerializer,
    QnaQuestionSerializer,
    SpecialistShopImageSerializer,
)
from .models import (
    CustomUser,
    Customer,
    Specialist,
    DayAvailability,
    DayOff,
    BarberShop,
    BarberShopImage,
    SpecialistShopImage,
    Barber,
    AppointmentTimeSlot,
    QnaAnswer,
    QnaQuestion,
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
    permission_classes = [DRFIsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    permission_classes = [DRFIsAuthenticated]

    def post(self, request):
        # Perform any logout actions if needed
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )


class UserView(GenericView):
    permission_classes = [DRFIsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class CustomerView(GenericView):
    permission_classes = [DRFIsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class SpecialistView(GenericView):
    permission_classes = [AllowAny]  # Allow registration without authentication
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer
    
    # Override specific methods to control permissions
    def get_permissions(self):
        # Only allow AllowAny for create method, require authentication for others
        if self.request.method == 'POST':
            return [AllowAny()]
        return [DRFIsAuthenticated()]


class DayAvailabilityView(GenericView):
    permission_classes = [DRFIsAuthenticated]
    queryset = DayAvailability.objects.all()
    serializer_class = DayAvailabilitySerializer


class DayOffView(GenericView):
    permission_classes = [DRFIsAuthenticated]
    queryset = DayOff.objects.all()
    serializer_class = DayOffSerializer


class BarberShopView(GenericView):
    permission_classes = [DRFIsAuthenticated]
    queryset = BarberShop.objects.all()
    serializer_class = BarberShopSerializer


class BarberShopImageView(GenericView):
    permission_classes = [DRFIsAuthenticated]
    queryset = BarberShopImage.objects.all()
    serializer_class = BarberShopImageSerializer
    allowed_methods = ["list", "retrieve", "create", "delete"]


class BarberView(GenericView):
    permission_classes = [DRFIsAuthenticated]
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer


class AppointmentTimeSlotView(GenericView):
    permission_classes = [DRFIsAuthenticated]
    queryset = AppointmentTimeSlot.objects.all()
    serializer_class = AppointmentTimeSlotSerializer


class QnaAnswerView(GenericView):
    permission_classes = [DRFIsAuthenticated]
    queryset = QnaAnswer.objects.all()
    serializer_class = QnaAnswerSerializer


class QnaQuestionView(GenericView):
    permission_classes = [DRFIsAuthenticated]
    queryset = QnaQuestion.objects.all()
    serializer_class = QnaQuestionSerializer
    allowed_methods = ["list", "retrieve", "create", "delete"]


class SpecialistShopImageView(viewsets.ModelViewSet):
    """
    CRUD operations for specialist shop images.
    """
    queryset = SpecialistShopImage.objects.all()
    serializer_class = SpecialistShopImageSerializer
    permission_classes = [AllowAny]  # Allow anyone to create shop images 

    def get_queryset(self):
        """Filter images by specialist_id query parameter if provided"""
        queryset = SpecialistShopImage.objects.all()
        specialist_id = self.request.query_params.get("specialist_id")
        if specialist_id is not None:
            queryset = queryset.filter(specialist_id=specialist_id)
        return queryset

    def create(self, request, *args, **kwargs):
        """Create a new specialist shop image, enforcing the 5-image limit per specialist"""
        specialist_id = request.data.get("specialist_id")
        
        # Check if the specialist exists
        specialist = get_object_or_404(Specialist, id=specialist_id)
        
        # Check if the specialist already has 5 images
        existing_count = SpecialistShopImage.objects.filter(specialist=specialist).count()
        if existing_count >= 5:
            return Response(
                {"detail": "A specialist can only have up to 5 shop images."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().create(request, *args, **kwargs)
