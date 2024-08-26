from chat.domain.entities import Message, MessageKey
from chat.infrastructure.dynamodb.message_repository import MessageRepository
from chat.infrastructure.mysql.chatroom_repository import ChatroomRepository
from chat.infrastructure.rabbitmq.message_event_broker import MessageEventBroker
from django.db import transaction
from shared.application.services import entity_update

from .chatroom_service import ChatroomService


class MessageService:
    """Represents a service of message."""

    def __init__(self, chatroom_service, message_repo, message_event_broker):
        self.message_repo: MessageRepository = message_repo
        self.message_event_broker: MessageEventBroker = message_event_broker
        self.chatroom_repo: ChatroomRepository = ChatroomRepository()
        self.message_rows_number = 50  # default settings
        self.chatroom_service: ChatroomService = chatroom_service

    @transaction.atomic
    def message_create(self, room_id: int, user_id: int, text: str) -> Message:
        self.chatroom_service._member_exists_of_user(room_id=room_id, user_id=user_id)
        entity = Message(room_id=room_id, user_id=user_id, text=text)
        chatroom = self.chatroom_service.chatroom_get(room_id=room_id, user_id=user_id)
        chatroom.last_message_timestamp = entity.created_timestamp
        _ = entity_update(self.chatroom_repo, chatroom)
        message = self.message_repo.save(entity=entity)
        # message fanout
        self.message_event_broker.message_fanout(room_id=room_id, message=message)
        return message

    def message_delete(self, room_id: int, user_id: int, created_timestamp: int):
        self.chatroom_service._member_exists_of_user(room_id=room_id, user_id=user_id)
        entity_message_key = MessageKey(room_id=room_id, created_timestamp=created_timestamp)
        message_key = self.message_repo.key(entity=entity_message_key)
        self.message_repo.delete_by_key(key=message_key)

    def messages_of_room(self, room_id: int, user_id: int, last_timestamp: int):
        self.chatroom_service._member_exists_of_user(room_id=room_id, user_id=user_id)
        messages, last_timestamp = self.message_repo.messages_of_room(
            room_id=room_id, last_timestamp=last_timestamp, limit=self.message_rows_number
        )
        return messages, last_timestamp
