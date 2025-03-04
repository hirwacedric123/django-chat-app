

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from chat.routing import wsPatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websockets.settings')

http_response_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": http_response_app,
    "websocket":(
        URLRouter(
            wsPatterns
        )
    ),
})
