from account.application.email_service import EmailService
from account.application.token_service import TokenService
from account.application.user_service import UserService
from account.infrastructure.mysql.email_repository import EmailRepository
from account.infrastructure.mysql.user_repository import UserRepository
from config.django.base import JWT_EXPIRATION_DELTA_SECONDS, JWT_ISSUSER, JWT_SECRET_KEY

eamil_repo = EmailRepository()

user_repo = UserRepository()

token_service: TokenService = TokenService(
    user_repo=user_repo,
    jwt_secret_key=JWT_SECRET_KEY,
    jwt_exp_delta_seconds=JWT_EXPIRATION_DELTA_SECONDS,
    jwt_issuer=JWT_ISSUSER,
)

user_service: UserService = UserService(user_repo=user_repo, email_repo=eamil_repo)

email_service: EmailService = EmailService(email_repo=eamil_repo)
