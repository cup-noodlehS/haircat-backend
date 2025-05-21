from django.urls import path
from .webhooks import WebhookConsumer

websocket_urlpatterns = [
    path("ws/webhooks/", WebhookConsumer.as_asgi()),
] 