import pika
import subprocess

# Conecta ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declara os tópicos
channel.exchange_declare(exchange='cpu_temperature', exchange_type='fanout')
channel.exchange_declare(exchange='fire_detection', exchange_type='fanout')
channel.exchange_declare(exchange='fire_prevention', exchange_type='fanout')

# Define o limite de temperatura
temperature_limit = 70

# Cria a fila e se inscreve no tópico
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='cpu_temperature', queue=queue_name)

# Verifica a temperatura a cada mensagem recebida
def callback(ch, method, properties, body):
    temperature = float(body)
    if temperature > temperature_limit:
        # Publica mensagem de detecção de incêndio
        channel.basic_publish(exchange='fire_detection', routing_key='', body='Fire detected!')

        # Publica mensagem de ativação do sistema de prevenção de incêndio
        channel.basic_publish(exchange='fire_prevention', routing_key='', body='Activate fire prevention system!')

        # Dispara alarme sonoro ou luminoso (não implementado)
        print('Fire detected! Activate fire prevention system!')

# Se inscreve na fila e começa a consumir as mensagens
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
