from django.urls import path

from articles.consumers import YourConsumer

websocket_urlpatterns = [
    path('ws/some_path/', YourConsumer.as_asgi()),
]