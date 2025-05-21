"""
ASGI config for haircat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import sys
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Set up Django before importing modules that depend on Django models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "haircat.settings")

# Import custom channel layers if specified
channel_layers_module = os.environ.get("CHANNEL_LAYERS_MODULE")
if channel_layers_module:
    try:
        channel_layers = __import__(channel_layers_module, fromlist=["CHANNEL_LAYERS"])
        if hasattr(channel_layers, "CHANNEL_LAYERS"):
            # Override the CHANNEL_LAYERS setting
            from django.conf import settings
            settings.CHANNEL_LAYERS = channel_layers.CHANNEL_LAYERS
    except ImportError:
        print(f"Warning: Could not import {channel_layers_module}")

django.setup()

# Import after Django is set up
from general import routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        )
    ),
})
