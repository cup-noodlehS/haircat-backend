from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    UserProfileView,
    LogoutView,
    UserView,
    CustomerView,
    SpecialistView,
    DayAvailabilityView,
    DayOffView,
    BarberShopView,
    BarberShopImageView,
)
from .throttling import UserLoginRateThrottle
from rest_framework.throttling import AnonRateThrottle

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        CustomTokenObtainPairView.as_view(
            throttle_classes=[UserLoginRateThrottle, AnonRateThrottle]
        ),
        name="login",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", UserProfileView.as_view(), name="user_profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "users/", UserView.as_view({"get": "list", "post": "create"}), name="user-list"
    ),
    path(
        "users/<int:pk>/",
        UserView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="user-detail",
    ),
    path(
        "customers/",
        CustomerView.as_view({"get": "list", "post": "create"}),
        name="customer-list",
    ),
    path(
        "customers/<int:pk>/",
        CustomerView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="customer-detail",
    ),
    path(
        "specialists/",
        SpecialistView.as_view({"get": "list", "post": "create"}),
        name="specialist-list",
    ),
    path(
        "specialists/<int:pk>/",
        SpecialistView.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="specialist-detail",
    ),
    path(
        "day-availabilities/",
        DayAvailabilityView.as_view({"get": "list", "post": "create"}),
        name="day-availability-list",
    ),
    path(
        "day-availabilities/<int:pk>/",
        DayAvailabilityView.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="day-availability-detail",
    ),
    path(
        "day-offs/",
        DayOffView.as_view({"get": "list", "post": "create"}),
        name="day-off-list",
    ),
    path(
        "day-offs/<int:pk>/",
        DayOffView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="day-off-detail",
    ),
    path(
        "barber-shops/",
        BarberShopView.as_view({"get": "list", "post": "create"}),
        name="barber-shop-list",
    ),
    path(
        "barber-shops/<int:pk>/",
        BarberShopView.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="barber-shop-detail",
    ),
    path(
        "barber-shop-images/",
        BarberShopImageView.as_view({"get": "list", "post": "create"}),
        name="barber-shop-image-list",
    ),
    path(
        "barber-shop-images/<int:pk>/",
        BarberShopImageView.as_view(
            {"get": "retrieve", "delete": "destroy"}
        ),
        name="barber-shop-image-detail",
    ),
    
]
