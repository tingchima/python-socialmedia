from account.domain.entities import Email as EmailEntity
from account.models import Email as EmailModel
from shared.infrastructure.data_meappers import DataMapper
from shared.infrastructure.repositories import DjangoRepository


class EmailDataMapper(DataMapper):
    """Represents a data mapper of Email."""

    def model_to_entity(self, model: EmailModel) -> EmailEntity:
        return EmailEntity(
            id=model.id,
            user_id=model.user_id,
            status=model.status,
            sent_at=model.sent_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def entity_to_model(self, entity: EmailEntity) -> EmailModel:
        return EmailModel(
            id=entity.id,
            user_id=entity.user_id,
            status=entity.status,
            sent_at=entity.sent_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class EmailRepository(DjangoRepository):
    """Represents a repository of Email."""

    data_mapper_cls = EmailDataMapper

    model_cls = EmailModel
