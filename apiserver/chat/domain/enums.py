from enum import Enum


class RoomType(Enum):
    """Represents a type of chatroom enum."""

    SINGLE = 1
    GROUP = 2
    OFFICIAL = 3

    @property
    def is_single_chatroom(self) -> bool:
        return self == RoomType.SINGLE

    @property
    def is_group_chatroom(self) -> bool:
        return self == RoomType.GROUP

    @property
    def is_official_chatroom(self) -> bool:
        return self == RoomType.OFFICIAL
