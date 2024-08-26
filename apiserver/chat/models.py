from dataclasses import dataclass

from account.models import User
from django.db import models
from shared.models import Base


class Chatroom(Base):
    """Represents a chatroom model."""

    class Meta:
        db_table_comment = "chatroom data"
        db_table = "chatrooms"

    class RoomType(models.IntegerChoices):
        """Represents a room type choices."""

        SINGLE = 1
        GROUP = 2
        OFFICIAL = 3

    room_name = models.CharField(
        unique=True,
        max_length=255,
        db_comment="chatroom name",
    )
    avatar_url = models.URLField(
        default="",
        db_comment="avatar url of chatroom",
    )
    room_type = models.CharField(
        max_length=10,
        choices=RoomType,
        default=RoomType.SINGLE,
        db_comment="type of chatroom",
    )
    last_message_timestamp = models.BigIntegerField(
        null=True,
        default=0,
        db_comment="the last message of created at timestmap",
    )

    def __str__(self):
        return f"{self.room_type} {self.room_name}"


class ChatroomMember(Base):
    """Represents a chatroom member model."""

    class Meta:
        db_table_comment = "member data in the chatroom"
        db_table = "chatroom_members"

    room = models.ForeignKey(
        Chatroom,
        on_delete=models.CASCADE,
        related_name="room",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    leaved_at = models.DateTimeField(
        null=True,
    )


class Message:
    """Represetns a model of message."""

    table_name = "messages"

    # room_id: int
    # created_timestamp: int
    # user_id: int
    # text: str


@dataclass
class MessageKey:
    """Represnets a key of message model."""

    room_id: int
    created_timestamp: int
