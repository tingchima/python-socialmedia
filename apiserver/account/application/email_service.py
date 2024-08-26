from account.domain.entities import Email
from account.infrastructure.mysql.email_repository import EmailRepository
from django.db import transaction


class EmailService:
    """Represents a service of email."""

    def __init__(self, email_repo):
        self.email_repo: EmailRepository = email_repo

    def email_get_by_id(self, id: int) -> Email:
        email = self.email_repo.get_by_key(id=id)
        return email

    @transaction.atomic
    def email_send(self, email: Email) -> Email:
        print(f"email send by {email.id}")
        print("......")
        print("sending...")
        print("update SENT status")
        print("......")
        print("......")
        print(f"email send completely by {email.id}")

    @transaction.atomic
    def email_failed(self, email: Email) -> Email:
        print(f"email failed by {email.id}")
        print("......")
        print("......")
        print("update FAILED status")
        print("......")
        print("......")
        print(f"email failed completely by {email.id}")
