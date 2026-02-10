from consumer_interface import mqConsumerInterface
import pika
import os

class mqConsumer(mqConsumerInterface):
    def __init__(self, binding_key: str, exchange_name: str, queue_name: str) -> None:
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        setupRMQConnection()

    def setupRMQConnection(self):
        # Setup connection to rabbitmq
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        connection = pika.BlockingConnection(parameters=con_params)
        channel = connection.channel()

        # Declare the exchange
        exchange = channel.exchange_declare(exchange=self.exchange_name)

        # Declare the queue
        channel.queue_declare(queue="Queue Name")

        channel.queue_bind(
        queue= "Queue Name",
        routing_key= "Routing Key",
        exchange="Exchange Name",
)
        channel.basic_consume("Queue Name", Function Name, auto_ack=False)

    def on_message_callback(self, channel, method_frame, header_frame, body) -> None:
        pass

    def startConsuming(self) -> None:
        
