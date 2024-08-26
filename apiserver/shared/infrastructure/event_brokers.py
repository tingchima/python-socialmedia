from pika import SelectConnection, URLParameters


class RabbitMqEvnetBroker:
    """Represents a event broker of rabbitmq."""


class PikaPublisher:
    """Represnets a publisher of pika."""

    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url

    def connect(self):
        return SelectConnection(
            parameters=URLParameters(self.amqp_url),
            on_open_callback=self.on_open_callback,
        )

    def on_open_callback(self, _unused_connection):
        print("on_open_callback")


# amqp_url = "amqp://guest:guest@localhost:5672/"
# publisher = PikaPublisher(amqp_url=amqp_url)
# conn = publisher.connect()
# print(f"amqp_conn={conn}")
