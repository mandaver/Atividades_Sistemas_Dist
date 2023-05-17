import pika
from termcolor import colored

# Conecta ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # Conecta ao servidor RabbitMQ local
channel = connection.channel()  # Cria um canal de comunicação

# Declara o tópico de temperatura e o tópico de incêndio
channel.queue_declare(queue='temperature')  # Declara a fila "temperature" para receber mensagens de temperatura
channel.queue_declare(queue='fire_alert')  # Declara a fila "fire_alert" para receber mensagens de alerta de incêndio

# Define a função de callback para lidar com as mensagens recebidas
def callback(ch, method, properties, body):
    temperature = float(body)
    if temperature > 50:
        # Se a temperatura for maior que 50 graus Celsius, publica uma mensagem no tópico de incêndio
        channel.basic_publish(exchange='', routing_key='fire_alert', body='FIRE DETECTED!')
        print(colored('Incêndio detectado!', 'red'))  # Exibe uma mensagem de incêndio detectado em vermelho
    else:
        print('Temperature:', temperature)  # Exibe a temperatura normalmente

# Registra a função de callback no tópico de temperatura
channel.basic_consume(queue='temperature', on_message_callback=callback, auto_ack=True)

# Inicia o loop de espera por mensagens
print('Aguardando tarefas...')
channel.start_consuming()  # Inicia o consumo das mensagens do RabbitMQ
