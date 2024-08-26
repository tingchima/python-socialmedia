from datetime import datetime, timedelta, timezone

import jwt
from shared.domain.errors import UnauthorizedError

from ..domain.entities import Token, User
from ..domain.enums import SOCIALMEDIA_APP, SOCIALMEDIA_WEB
from ..infrastructure.mysql.user_repository import UserRepository


class TokenService:
    """Represents a service of token."""

    def __init__(
        self,
        user_repo,
        jwt_secret_key: str,
        jwt_issuer: str,
        jwt_exp_delta_seconds: int,
    ):
        self.user_repo: UserRepository = user_repo
        self.jwt_secret = jwt_secret_key
        self.jwt_iss = jwt_issuer
        self.jwt_exp_delta_seconds = jwt_exp_delta_seconds
        self.jwt_refresh_exp_delta_seconds = self.jwt_exp_delta_seconds * 2
        self.jwt_algo = "HS256"

    def _token_create(self, user_id: int, client_id: str, exp_delta_secions: int) -> str:
        now = datetime.now(timezone.utc)
        claims = {
            "iss": self.jwt_iss,  # jwt簽發者
            "sub": user_id,  # jwt使用者
            "aud": client_id,  # 接收jwt的一方
            "iat": now,  # jwt簽發時間
            "exp": now + timedelta(seconds=exp_delta_secions),
        }
        return jwt.encode(claims, self.jwt_secret, algorithm=self.jwt_algo)

    def client_id_verify(self, client_id: str) -> bool:
        if client_id == SOCIALMEDIA_WEB or client_id == SOCIALMEDIA_APP:
            return True
        raise UnauthorizedError

    def token_create(self, email: str, client_id: str) -> Token:
        user = self.user_repo.user_get_by_email(email=email)
        return Token(
            access_token=self._token_create(
                user.id,
                client_id,
                self.jwt_exp_delta_seconds,
            ),
            refresh_token=self._token_create(
                user.id,
                client_id,
                self.jwt_refresh_exp_delta_seconds,
            ),
        )

    def token_refresh(self, token: str, client_id: str) -> Token:
        user = self.token_verify(token, client_id)
        token = self.token_create(user.email, client_id)
        return token

    def token_verify(self, token: str, client_id: str) -> User:
        try:
            claims = jwt.decode(
                jwt=token,
                key=self.jwt_secret,
                algorithms=self.jwt_algo,
                issuer=self.jwt_iss,
                audience=client_id,
            )
            user = self.user_repo.get_by_key(id=dict(claims)["sub"])
        except Exception as e:
            raise UnauthorizedError(e)

        return user
