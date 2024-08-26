from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from shared.domain.entities import Entity

from .enums import EmailStatus, UserType


@dataclass
class Token(Entity):
    """Represents a token entity."""

    access_token: str
    refresh_token: str


@dataclass
class User(Entity):
    """Represents a user entity."""

    email: str
    password: str
    user_type: UserType
    avatar_url: str

    id: int = None
    username: str = None
    is_disabled: bool = False
    disabled_at: datetime = None
    created_at: datetime = None
    updated_at: datetime = None

    @classmethod
    def new(
        cls,
        email: str,
        username: str,
        password: str,
        avatar_url: str,
        user_type: UserType,
    ) -> User:
        return cls(
            email=email,
            username=username,
            password=password,
            avatar_url=avatar_url,
            user_type=user_type,
        )


@dataclass
class Email(Entity):
    """Represents a entity of email."""

    user_id: int
    status: EmailStatus

    id: int = None
    sent_at: datetime = None
    created_at: datetime = None
    updated_at: datetime = None
