from dataclasses import dataclass
from datetime import datetime

from django.utils import timezone
from shared.domain.entities import Entity

from .enums import RoomType


@dataclass
class Chatroom(Entity):
    """Represents an entitiy of chatroom."""

    room_name: str
    room_type: RoomType
    avatar_url: str

    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    last_message_timestamp: int | None = None


@dataclass
class ChatroomMember(Entity):
    """Represents an entitiy of chatroom member ."""

    room_id: int
    user_id: int

    id: int | None = None
    leaved_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Message(Entity):
    """Represents an entitiy of message."""

    def __init__(self, room_id: int, user_id: int, text: str, created_timestamp: int = None):
        self.room_id = room_id
        self.user_id = user_id
        self.text = text
        self.created_timestamp = (
            created_timestamp if created_timestamp else int(timezone.now().timestamp() * 1e9)
        )


@dataclass
class MessageKey:
    """Represents an entity of message key."""

    room_id: int
    created_timestamp: int
