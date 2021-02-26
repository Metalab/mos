from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({

    "websocket": AuthMiddlewareStack(
        URLRouter([
        ])
    ),
})
