from account.domain.entities import User as User
from account.models import User as UserModel
from shared.domain.errors import NotFoundError
from shared.infrastructure.data_meappers import DataMapper
from shared.infrastructure.repositories import DjangoRepository


class UserDataMapper(DataMapper):
    """Represents a data mapper of user."""

    def model_to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email_address,
            password=model.password,
            user_type=model.user_type,
            avatar_url=model.avatar_url,
            is_disabled=model.is_disabled,
            disabled_at=model.disabled_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def entity_to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            username=entity.username,
            email_address=entity.email,
            password=entity.password,
            user_type=entity.user_type,
            avatar_url=entity.avatar_url,
            is_disabled=entity.is_disabled,
            disabled_at=entity.disabled_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class UserRepository(DjangoRepository):
    """Represents a repository of user."""

    data_mapper_cls = UserDataMapper

    model_cls = UserModel

    def user_get_by_email(self, email: str) -> User:
        try:
            model = UserModel.objects.get(email_address=email)
        except UserModel.DoesNotExist:
            raise NotFoundError("specified user not found by email")
        return self.data_mapper.model_to_entity(model=model)
