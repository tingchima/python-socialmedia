import json
import threading
from dataclasses import dataclass

from channels.generic.websocket import WebsocketConsumer
from pika import BlockingConnection, URLParameters
from pika.exchange_type import ExchangeType

from .containers import rabbitmq_url


@dataclass
class Message:

    room_id: int
    user_id: int
    text: str
    created_timestamp: int


class ChatroomConsumer(WebsocketConsumer):

    def _on_message_callback(self, channel, method, properties, body):
        message = json.loads(body, object_hook=lambda d: Message(**d))
        self.send(text_data=json.dumps(message.__dict__))

    def consumer_in_background(self):
        self.ch.basic_consume(
            queue=self.queue_name,
            auto_ack=True,
            on_message_callback=self._on_message_callback,
        )
        self.ch.start_consuming()

    def connect(self):
        self.rabbitmq = BlockingConnection(parameters=URLParameters(rabbitmq_url))
        self.ch = self.rabbitmq.channel()

        # room_id / user_id
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]

        # accept connection
        self.accept()

        # bind rabbitmq queue
        exchange = "room_{}".format(str(self.room_id))
        self.ch.exchange_declare(exchange=exchange, exchange_type=ExchangeType.fanout, durable=True)
        self.queue_name = "{}_user_{}".format(exchange, str(self.user_id))

        self.ch.queue_declare(
            queue=self.queue_name,  # queue name
            exclusive=True,  # kill queue when connection is closed
            arguments={"max-length-bytes": 1048576},  # 1mb length
        )
        self.ch.queue_bind(exchange=exchange, queue=self.queue_name)

        task = threading.Thread(target=self.consumer_in_background)
        task.start()

    def disconnect(self, close_code):
        self.ch.stop_consuming()
        self.ch.queue_delete(queue=self.queue_name)
        self.ch.close()
        self.close()
