import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import EasyMarketProducts.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EasyMarket.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            EasyMarketProducts.routing.websocket_urlpatterns
        )
    ),
})