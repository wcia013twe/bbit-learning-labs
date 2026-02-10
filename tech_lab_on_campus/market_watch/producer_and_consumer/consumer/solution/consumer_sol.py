from consumer_interface import mqConsumerInterface
import pika
import os

class mqConsumer(mqConsumerInterface):
    
    def __init__(self, binding_key: str, exchange_name: str, queue_name: str) -> None:
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.connection, self.channel = self.setupRMQConnection()

    def setupRMQConnection(self):
        # Setup connection to rabbitmq
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        connection = pika.BlockingConnection(parameters=con_params)
        channel = connection.channel()

        # Declare the exchange
        exchange = channel.exchange_declare(exchange=self.exchange_name)

        # Declare the queue
        channel.queue_declare(queue=self.queue_name)

        # bind the binding key to the queue on the exchange
        channel.queue_bind(
            queue= self.queue_name,
            routing_key= self.binding_key,
            exchange=self.exchange_name,
        )

        channel.basic_consume(self.queue_name, self.on_message_callback, auto_ack=False) 
        return connection, channel

    def on_message_callback(self, channel, method_frame, header_frame, body) -> None:
        self.channel.basic_ack(method_frame.delivery_tag, False)
        print(body)

    def startConsuming(self) -> None:
        print(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()


    def __del__(self) -> None:
        # Print "Closing RMQ connection on destruction"
        print("Closing RMQ connection on destruction")

        # Close Channel
        self.channel.close()

        # Close Connection
        self.connection.close()
        

        
