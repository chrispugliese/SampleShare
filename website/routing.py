from django.urls import path
from . import consumers  # Ensure you have a consumers.py file in the same app
#This will map WebSocket connections to ChatConsumer.
websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]
