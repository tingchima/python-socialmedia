from config.django.base import (
    RABBITMQ_HOST,
    RABBITMQ_PASSWORD,
    RABBITMQ_PORT,
    RABBITMQ_SCHEME,
    RABBITMQ_USERNAME,
    RABBITMQ_VIRTUAL_HOST,
)

rabbitmq_url = "{}://{}:{}@{}:{}{}".format(
    RABBITMQ_SCHEME,
    RABBITMQ_USERNAME,
    RABBITMQ_PASSWORD,
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_VIRTUAL_HOST,
)
