from django.urls import path
from hairstyle.views.service import (
    ServiceView,
    ServiceLabelView,
    ServiceImageView,
    LabelView,
)
from hairstyle.views import (
    AppointmentView,
    ReviewView,
    ReviewImageView,
    AppointmentMessageView,
    AppointmentMessageThreadView,
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
    path(
        "appointments/",
        AppointmentView.as_view({"get": "list", "post": "create"}),
        name="appointment-list",
    ),
    path(
        "appointments/<int:pk>/",
        AppointmentView.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="appointment-detail",
    ),
    path(
        "reviews/",
        ReviewView.as_view({"get": "list", "post": "create"}),
        name="review-list",
    ),
    path(
        "reviews/<int:pk>/",
        ReviewView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="review-detail",
    ),
    path(
        "review-images/",
        ReviewImageView.as_view({"get": "list", "post": "create"}),
        name="review-image-list",
    ),
    path(
        "review-images/<int:pk>/",
        ReviewImageView.as_view({"delete": "destroy"}),
        name="review-image-detail",
    ),
    path(
        "appointment-message-threads/",
        AppointmentMessageThreadView.as_view({"get": "list", "post": "create"}),
        name="appointment-message-thread-list",
    ),
    path(
        "appointment-message-threads/<int:pk>/",
        AppointmentMessageThreadView.as_view({"get": "retrieve"}),
        name="appointment-message-thread-detail",
    ),
    path(
        "appointment-message-threads/<int:thread_id>/messages/",
        AppointmentMessageView.as_view({"get": "list", "post": "send_message"}),
        name="appointment-message-list",
    ),
]
