# chat/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/tour/<int:tour_id>/', consumers.TourChatConsumer.as_asgi()),
]

