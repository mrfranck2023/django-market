from channels.routing import ProtocolTypeRouter, URLRouter
import EasyMarketProducts.routing

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        EasyMarketProducts.routing.websocket_urlpatterns
    ),
})