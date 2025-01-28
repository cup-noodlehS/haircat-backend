from django.urls import path
from hairstyle.views.service import (
    ServiceView,
    ServiceLabelView,
    ServiceImageView,
    LabelView,
)

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
    path(
        "service-labels/",
        ServiceLabelView.as_view({"get": "list", "post": "create"}),
        name="service-label-list",
    ),
    path(
        "service-labels/<int:pk>/",
        ServiceLabelView.as_view({"delete": "destroy"}),
        name="service-label-detail",
    ),
    path(
        "service-images/",
        ServiceImageView.as_view({"get": "list", "post": "create"}),
        name="service-image-list",
    ),
    path(
        "service-images/<int:pk>/",
        ServiceImageView.as_view({"delete": "destroy"}),
        name="service-image-detail",
    ),
    path(
        "labels/",
        LabelView.as_view({"get": "list", "post": "create"}),
        name="label-list",
    ),
    path(
        "labels/<int:pk>/",
        LabelView.as_view({"get": "retrieve", "delete": "destroy"}),
        name="label-detail",
    ),
]
