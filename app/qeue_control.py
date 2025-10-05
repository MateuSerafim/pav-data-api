import pika
import os
def send_to_queue(queue_name: str, message: str):
    params = pika.URLParameters(os.getenv("RABBITMQ_URL"))
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    
    channel.queue_declare(queue=queue_name, durable=True)
    
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)  # persistente
    )
    connection.close()