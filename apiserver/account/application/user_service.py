from account.domain.entities import User

# from account.domain.enums import EmailStatus
from account.infrastructure.mysql.email_repository import EmailRepository
from account.infrastructure.mysql.user_repository import UserRepository
from django.db import transaction


class UserService:
    """Represents a service of user."""

    def __init__(self, user_repo, email_repo):
        self.user_repo: UserRepository = user_repo
        self.email_repo: EmailRepository = email_repo

    @transaction.atomic
    def user_create(self, param: User) -> User:
        user = self.user_repo.save(param)
        return user

    def user_get_by_email(self, email: str) -> User:
        user = self.user_repo.user_get_by_email(email)
        return user
