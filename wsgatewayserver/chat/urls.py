from django.urls import path

from .websocket_consumer import ChatroomConsumer

urlpatterns = []


websocket_urlpatterns = [
    path("ws/users/<int:user_id>/chatrooms/<int:room_id>", ChatroomConsumer.as_asgi()),
]
