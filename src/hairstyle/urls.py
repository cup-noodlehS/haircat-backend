from django.urls import path
from hairstyle.views.service import ServiceView

urlpatterns = [
    path(
        "services/",
        ServiceView.as_view({"get": "list", "post": "create"}),
        name="service-list",
    ),
    path(
        "services/<int:pk>/",
        ServiceView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="service-detail",
    ),
]
