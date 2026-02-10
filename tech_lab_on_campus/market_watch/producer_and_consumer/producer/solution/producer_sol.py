import pika, os
from producer_interface import mqProducerInterface  # pylint: disable=import-error

class mqProducer(mqProducerInterface):

    def __init__(self, routing_key: str, exchange_name: str) -> None:
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        self.connection, self.channel = self.setupRMQConnection()
        

    def setupRMQConnection(self) -> None:
        conParams = pika.URLParameters(os.environ['AMQP_URL'])
        connection = pika.BlockingConnection(parameters=conParams)
        channel = connection.channel()
        channel.exchange_declare(self.exchange_name)
        return connection, channel

    def publishOrder(self, message: str) -> None:
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message
        )
        print("Successfully sent the message")
    