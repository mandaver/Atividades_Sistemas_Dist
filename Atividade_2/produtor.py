import pika
import psutil
import time

# Conecta ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # Conecta ao servidor RabbitMQ local
channel = connection.channel()  # Cria um canal de comunicação

# Declara o tópico de temperatura
channel.queue_declare(queue='temperature')  # Declara a fila "temperature" para receber mensagens de temperatura

def publish_temp_cpu():
    # Publica a temperatura da CPU no tópico
    temperature = psutil.sensors_temperatures()['coretemp'][0].current  # Obtém a temperatura atual da CPU
    channel.basic_publish(exchange='', routing_key='temperature', body=str(temperature))  # Publica a temperatura no tópico "temperature"

while True:
    publish_temp_cpu()  # Chama a função para publicar a temperatura da CPU no tópico
    time.sleep(3)  # Espera por 3 segundos antes de publicar a próxima temperatura

