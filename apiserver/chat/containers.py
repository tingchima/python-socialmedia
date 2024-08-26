import boto3
from chat.application.chatroom_service import ChatroomService
from chat.application.message_service import MessageService
from chat.infrastructure.dynamodb.message_repository import MessageRepository
from chat.infrastructure.rabbitmq.message_event_broker import MessageEventBroker
from config.django.base import (
    AWS_DYNAMODB_LOCAL,
    AWS_REGION_NAME,
    RABBITMQ_HOST,
    RABBITMQ_PASSWORD,
    RABBITMQ_PORT,
    RABBITMQ_SCHEME,
    RABBITMQ_USERNAME,
    RABBITMQ_VIRTUAL_HOST,
)
from pika import BlockingConnection, URLParameters

amqp_url = "{}://{}:{}@{}:{}{}".format(
    RABBITMQ_SCHEME,
    RABBITMQ_USERNAME,
    RABBITMQ_PASSWORD,
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_VIRTUAL_HOST,
)
rabbitmq = BlockingConnection(parameters=URLParameters(amqp_url))

dynamodb = boto3.resource(
    service_name="dynamodb",
    endpoint_url=AWS_DYNAMODB_LOCAL,
    region_name=AWS_REGION_NAME,
)

message_repo = MessageRepository(dynamodb=dynamodb)

message_event_broker = MessageEventBroker(rabbitmq=rabbitmq)

chatroom_service: ChatroomService = ChatroomService()

message_service: MessageService = MessageService(
    chatroom_service=chatroom_service,
    message_repo=None,
    message_event_broker=None,
)
