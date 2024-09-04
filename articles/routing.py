from django.urls import re_path

from .consumers import SocketteConsumer

websocket_urlpatterns = [
    re_path(r'ws/sockette/$', SocketteConsumer.as_asgi()),
]