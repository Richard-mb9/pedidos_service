import pika


def callback(ch, method, properties, body):
    print(f" [x] Recebido: {body.decode()}")
    # Confirma o processamento (opcional, mas recomendado)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
    # 1. Configurações de Conexão
    credentials = pika.PlainCredentials("guest", "guest")
    parameters = pika.ConnectionParameters(
        host="localhost", port=5673, credentials=credentials
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # 2. Garante que o Exchange existe
    channel.exchange_declare(exchange="orders", exchange_type="topic", durable=True)

    # 3. Cria uma fila exclusiva para este consumer
    result = channel.queue_declare(queue="orders_queue", durable=True)
    queue_name = result.method.queue

    # 4. Vincula a fila ao Exchange (usando '#' para receber tudo do exchange)
    channel.queue_bind(exchange="orders", queue=queue_name, routing_key="#")

    print(" [*] Aguardando mensagens. Para sair pressione CTRL+C")

    # 5. Define qual função processa as mensagens
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()


if __name__ == "__main__":
    start_consumer()
