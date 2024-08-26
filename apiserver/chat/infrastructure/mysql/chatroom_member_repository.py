from chat.domain.entities import ChatroomMember as ChatroomMemberEntity
from chat.models import ChatroomMember as ChatroomMemberModel
from django.db import DatabaseError
from shared.domain.errors import InternalServerError
from shared.infrastructure.data_meappers import DataMapper
from shared.infrastructure.repositories import DjangoRepository


class ChatroomMemberDataMapper(DataMapper):
    """Represnets a data mapper of chatroom."""

    def model_to_entity(self, model: ChatroomMemberModel) -> ChatroomMemberEntity:
        return ChatroomMemberEntity(
            id=model.id,
            room_id=model.room_id,
            user_id=model.user_id,
            leaved_at=model.leaved_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def entity_to_model(self, entity: ChatroomMemberEntity) -> ChatroomMemberModel:
        return ChatroomMemberModel(
            id=entity.id,
            room_id=entity.room_id,
            user_id=entity.user_id,
            leaved_at=entity.leaved_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class ChatroomMemberRepository(DjangoRepository):
    """Represents a repository of chatroom member."""

    model_cls = ChatroomMemberModel

    data_mapper_cls = ChatroomMemberDataMapper

    def member_exists_of_user(self, room_id: int, user_id: int) -> bool:
        try:
            query_set = ChatroomMemberModel.objects.filter(
                room_id=room_id,
                user_id=user_id,
            )
            return query_set.exists()
        except DatabaseError as e:
            raise InternalServerError(e)
