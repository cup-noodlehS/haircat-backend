from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    UserProfileView,
    LogoutView,
    UserView,
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
]
