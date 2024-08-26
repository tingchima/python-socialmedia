from enum import Enum


class UserType(Enum):
    """Represents a type of chatroom enum."""

    COMMON = 1
    OFFICIAL = 2

    @property
    def is_common_user(self) -> bool:
        return self == UserType.COMMON

    @property
    def is_official_user(self) -> bool:
        return self == UserType.OFFICIAL


SOCIALMEDIA_WEB = "socialmedia_web"
SOCIALMEDIA_APP = "socialmedia_app"


class EmailStatus(Enum):
    """Represents a enum of email status."""

    READY = "READY", "Ready"
    SENDING = "SENDING", "Sending"
    SENT = "SENT", "Sent"
    FAILED = "FAILED", "Failed"
