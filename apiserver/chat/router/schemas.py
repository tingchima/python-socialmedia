from datetime import datetime
from typing import List

from chat.domain.entities import Chatroom as ChatroomEntity
from chat.domain.entities import Message as MessageEntity
from ninja import Schema


class Chatroom(Schema):
    """Represents a schema of chatroom."""

    room_id: int
    room_name: str
    room_type: str
    last_message_timestamp: int
    avatar_url: str
    created_at: datetime
    updated_at: datetime


class ChatroomListQuery(Schema):
    """Represents a schema of chatroom list query."""

    offset: int
    limit: int


class ChatroomListResponse(Schema):
    """Represents a shcema of chatroom list response."""

    rooms: List[Chatroom]
    next_offset: int

    @classmethod
    def build(cls, rooms: List[ChatroomEntity], next_offset: int) -> dict:
        return cls(
            rooms=[
                Chatroom(
                    room_id=room.id,
                    room_name=room.room_name,
                    room_type=room.room_type,
                    last_message_timestamp=int(room.last_message_timestamp or 0),
                    avatar_url=room.avatar_url,
                    created_at=room.created_at,
                    updated_at=room.updated_at,
                )
                for room in rooms
            ],
            next_offset=next_offset,
        ).model_dump()


class ChatroomCreateBody(Schema):
    """Represents a shcema of chatroom create body."""

    room_name: str
    room_type: str
    avatar_url: str


class ChatroomCreateResponse(Schema):
    """Represents a schema of chatroom create response."""

    room: Chatroom

    @classmethod
    def build(cls, room: ChatroomEntity) -> dict:
        print(f"room={room}")
        return cls(
            room=Chatroom(
                room_id=room.id,
                room_name=room.room_name,
                room_type=room.room_type,
                avatar_url=room.avatar_url,
                last_message_timestamp=int(room.last_message_timestamp or 0),
                created_at=room.created_at,
                updated_at=room.updated_at,
            ),
        ).model_dump()


class ChatroomJoinPath(Schema):
    """Represents a shcema of chatroom join path."""

    room_id: int


class ChatroomGetResposne(Schema):
    """Represents a chatroom get response."""

    room: Chatroom

    @classmethod
    def build(cls, room: ChatroomEntity) -> dict:
        return cls(
            room=Chatroom(
                room_id=room.id,
                room_name=room.room_name,
                room_type=room.room_type,
                avatar_url=room.avatar_url,
                created_at=room.created_at,
                updated_at=room.updated_at,
                last_message_timestamp=int(room.last_message_timestamp or 0),
            )
        ).model_dump()


class Message(Schema):
    """Represents a message."""

    room_id: int
    user_id: int
    text: str
    created_timestamp: int


class MessageListQuery(Schema):
    """Represents a schema of message list query."""

    room_id: int
    last_timestamp: int  # UTC+0


class MessageListResponse(Schema):
    """Represents a schema of message list response."""

    messages: List[Message]
    next_last_timestamp: int

    @classmethod
    def build(cls, messages: List[MessageEntity], last_timesatmp: int) -> dict:
        return cls(
            messages=[
                Message(
                    room_id=message.room_id,
                    user_id=message.user_id,
                    text=message.text,
                    created_timestamp=message.created_timestamp,
                )
                for message in messages
            ],
            next_last_timestamp=last_timesatmp,
        ).model_dump()


class MessageCreateBody(Schema):
    """Represents a schema of message chreate body."""

    room_id: int
    text: str


class MessageCreateResponse(Schema):
    """Represents a schema of message create response."""

    message: Message

    @classmethod
    def build(cls, message: MessageEntity) -> dict:
        return cls(
            message=Message(
                room_id=message.room_id,
                user_id=message.user_id,
                text=message.text,
                created_timestamp=message.created_timestamp,
            )
        ).model_dump()


class MessageDeleteBody(Schema):
    """Represents a schema of message delete body."""

    room_id: int
    created_timestamp: int
