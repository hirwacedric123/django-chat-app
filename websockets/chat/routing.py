from django.urls import path
from . import consumers
from .consumers import ChatConsumer

wsPatterns = [
    path('ws/messages/<str:room_name>/', ChatConsumer.as_asgi())
]