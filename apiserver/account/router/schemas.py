from datetime import datetime
from typing import Optional

from account.domain.entities import Token as TokenEntity
from account.domain.entities import User as User
from ninja import Schema


class Token(Schema):
    """Represents a token schema."""

    access_token: str
    refresh_token: str

    @classmethod
    def build(cls, token: TokenEntity) -> dict:
        return cls(
            access_token=token.access_token,
            refresh_token=token.refresh_token,
        ).model_dump()


class TokenCreateBody(Schema):
    """Represents a token create body schema."""

    email: str
    password: str
    client_id: str


class TokenRefreshBody(Schema):
    """Represents a token refresh body schema."""

    refresh_token: str


class TokenCreateResponse(Schema):
    """Represents a token create response schema."""

    token: Token

    @classmethod
    def build(cls, token: TokenEntity) -> dict:
        return cls(
            token=Token(
                access_token=token.access_token,
                refresh_token=token.refresh_token,
            ),
        ).model_dump()


class User(Schema):
    """Represents a user shcema."""

    user_id: int
    username: str
    email: str
    password: str
    user_type: str
    avatar_url: str
    is_disabled: bool
    disabled_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class UserCreateBody(Schema):
    """Represents a user create body schema."""

    email: str
    username: str
    password: str
    avatar_url: str
    user_type: str


class UserCreateReponse(Schema):
    """Represents a user create response schema."""

    user: User

    @classmethod
    def build(cls, user: User) -> dict:
        return cls(
            user=User(
                user_id=user.id,
                username=user.username,
                email=user.email,
                password=user.password,
                user_type=user.user_type,
                avatar_url=user.avatar_url,
                is_disabled=user.is_disabled,
                disabled_at=user.disabled_at,
                created_at=user.created_at,
                updated_at=user.updated_at,
            ),
        )
