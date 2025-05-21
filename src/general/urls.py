from django.urls import path
from general.views import FileView, LocationView, TestWebhookView

urlpatterns = [
    path(
        "files/", FileView.as_view({"get": "list", "post": "create"}), name="file-list"
    ),
    path(
        "files/<int:pk>/",
        FileView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="file-detail",
    ),
    path(
        "locations/",
        LocationView.as_view({"get": "list", "post": "create"}),
        name="location-list",
    ),
    path(
        "locations/<int:pk>/",
        LocationView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="location-detail",
    ),
    # Webhook endpoints
    path("webhooks/test/", TestWebhookView.as_view(), name="webhook-test"),
]
