import json

from chat.domain.entities import Message
from pika import BlockingConnection
from pika.exceptions import AMQPError
from shared.domain.errors import InternalServerError


class MessageEventBroker:
    """Represents a event broker of chatroom message."""

    def __init__(self, rabbitmq: BlockingConnection):
        self.channel = rabbitmq.channel()

    def _exchange_declare(self, exchange: str, exchange_type: str, durable: bool = False):
        self.channel.exchange_declare(
            exchange=exchange, exchange_type=exchange_type, durable=durable
        )

    def message_fanout(self, room_id: int, message: Message):
        try:
            body = json.dumps(message.__dict__)
            exchange = "room_{}".format(str(room_id))
            self._exchange_declare(exchange=exchange, exchange_type="fanout", durable=True)
            self.channel.basic_publish(exchange=exchange, routing_key="", body=body)
        except AMQPError as e:
            raise InternalServerError(e)
