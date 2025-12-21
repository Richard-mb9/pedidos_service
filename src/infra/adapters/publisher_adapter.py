from typing import Any, Dict
from json import dumps
from pika import (
    ConnectionParameters,
    BlockingConnection,
    PlainCredentials,
    BasicProperties,
)

from config import MQ_HOST, MQ_PASSWORD, MQ_USER, MQ_PORT
from application.adapters import PublisherAdapterInterface


class PublisherAdapter(PublisherAdapterInterface):
    def __init__(self, topic_name: str = "orders") -> None:
        self.connection = BlockingConnection(
            ConnectionParameters(
                host=MQ_HOST,
                port=int(MQ_PORT),
                credentials=PlainCredentials(MQ_USER, MQ_PASSWORD),
            )
        )
        self.topic_name = topic_name
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.topic_name, exchange_type="topic", durable=True
        )

    def publish(self, event_name: str, payload: Dict[str, Any]):
        self.channel.basic_publish(
            exchange=self.topic_name,
            routing_key=event_name,
            body=dumps(payload, default=str),
            properties=BasicProperties(
                content_type="application/json", delivery_mode=2
            ),
        )

        self.connection.close()
