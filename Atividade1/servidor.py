import socket # Biblioteca para comunicação em rede
import threading # Biblioteca para criar threads em Python
import hashlib #  Biblioteca para criptografar a mensagem original

# Define o endereço IP do servidor como localhost (127.0.0.1) e a porta como 55555
HOST = '127.0.0.1'
PORT = 55555

# Cria um objeto de socket para o servidor usando IPv4 e TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liga o socket à porta e ao endereço definidos anteriormente
server.bind((HOST, PORT))

# Cria uma lista vazia para armazenar todos os clientes conectados
clients = []

# Função que será executada em uma thread para lidar com as conexões dos clientes
def handle_client(client):
    while True:
        # Recebe a mensagem original e a mensagem criptografada do cliente
        message = client.recv(1024)
        encrypted_message = client.recv(1024)

        # Decodifica as mensagens recebidas de bytes para string
        message = message.decode()
        encrypted_message = encrypted_message.decode()

        # Criptografa a mensagem original usando o algoritmo SHA-256
        hashed_message = hashlib.sha256(message.encode()).hexdigest()

        # Envia a mensagem criptografada e a mensagem original para todos os outros clientes conectados
        for c in clients:
            if c != client:
                c.send(message.encode())
                c.send(hashed_message.encode())

        # Se a mensagem do cliente for "bye", desconecta o cliente
        if message == "bye":
            clients.remove(client)
            client.close()
            break

# Função para iniciar o servidor e aguardar por novas conexões
def start_server():
    # Inicia o servidor
    server.listen()

    while True:
        # Aguarda por novas conexões de clientes
        client, address = server.accept()

        # Adiciona o cliente à lista de clientes conectados
        clients.append(client)

        # Inicia uma nova thread para lidar com o cliente
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()

# Inicia o servidor chamando a função start_server()
start_server()
