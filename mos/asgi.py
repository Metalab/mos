"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django

from channels.routing import get_default_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from django.conf.urls import url

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.devel")
django.setup()

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
        ])
    ),
})
