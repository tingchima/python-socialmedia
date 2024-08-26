from boto3.dynamodb.conditions import Key
from boto3.exceptions import Boto3Error
from chat.domain.entities import Message as MessageEntity
from chat.models import Message as MessageModel
from chat.models import MessageKey
from shared.domain.errors import InternalServerError
from shared.infrastructure.data_meappers import JsonDataMapper
from shared.infrastructure.repositories import Boto3Repository


class MessageDataMapper(JsonDataMapper):
    """Represnets a data mapper of Message."""

    def json_data_to_entity(self, data: dict) -> MessageEntity:
        return MessageEntity(**data)

    def entity_to_json_data(self, entity: MessageEntity) -> dict:
        return dict(**entity.__dict__)


class MessageRepository(Boto3Repository):
    """Represents a repository of message."""

    _table_name = MessageModel().table_name
    data_mapper_cls = MessageDataMapper

    def __init__(self, dynamodb):
        self.table_cls = dynamodb.Table(self._table_name)

    def key(self, entity: MessageKey) -> dict:
        return dict(**entity.__dict__)

    def messages_of_room(self, room_id: int, last_timestamp: int, limit: int):
        try:
            result = self.table().query(
                KeyConditionExpression=(
                    Key("room_id").eq(room_id) & Key("created_timestamp").lt(last_timestamp)
                ),
                ScanIndexForward=(False),
                Limit=(limit),
            )
        except Boto3Error as e:
            raise InternalServerError(e)
        last_timestamp = 0
        if result.get("LastEvaluatedKey"):
            last_timestamp = result.get("LastEvaluatedKey").get("created_timestamp")
        messages = self.data_mapper.json_data_to_entity_list(data=result.get("Items"))
        return messages, last_timestamp
