from django.urls import path
from website import consumers  # Adjust to your app name

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),  # Adjust if necessary
]
