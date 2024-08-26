from chat.domain.entities import Chatroom as ChatroomEntity
from chat.models import Chatroom as ChatroomModel
from django.db import DatabaseError
from shared.domain.errors import InternalServerError
from shared.infrastructure.data_meappers import DataMapper
from shared.infrastructure.repositories import (
    DjangoRepository,
    offset_and_limit_to_start_and_end_index,
)


class ChatroomDataMapper(DataMapper):
    """Represnets a data mapper of chatroom."""

    def model_to_entity(self, model: ChatroomModel) -> ChatroomEntity:
        return ChatroomEntity(
            id=model.id,
            room_name=model.room_name,
            room_type=model.room_type,
            avatar_url=model.avatar_url,
            last_message_timestamp=model.last_message_timestamp,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def entity_to_model(self, entity: ChatroomEntity) -> ChatroomModel:
        return ChatroomModel(
            id=entity.id,
            room_name=entity.room_name,
            room_type=entity.room_type,
            avatar_url=entity.avatar_url,
            last_message_timestamp=entity.last_message_timestamp,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class ChatroomRepository(DjangoRepository):
    """Represents a repository of chatroom."""

    model_cls = ChatroomModel
    data_mapper_cls = ChatroomDataMapper

    def chatroom_exists_by_id(self, id: int) -> bool:
        try:
            query = ChatroomModel.objects.filter(id=id)
            return query.exists()
        except DatabaseError as e:
            raise InternalServerError(e)

    def chatrooms_of_user(self, user_id: int, offset: int, limit: int):
        try:
            start, end = offset_and_limit_to_start_and_end_index(offset=offset, limit=limit)
            query = ChatroomModel.objects.filter(room__user_id=user_id).prefetch_related("room")
            total_size = query.count()
            models = query.order_by("-last_message_timestamp", "created_at")[start:end]
            rooms = self.data_mapper.model_to_entity_list(models=models)
        except DatabaseError as e:
            raise InternalServerError(e)
        return rooms, total_size

    def chatroom_update_last_message_timestamp(self, room_id: int, last_message_timestamp: int):
        model = ChatroomModel(room_id=room_id).last_message_timestamp = last_message_timestamp
        model.save()
        return
