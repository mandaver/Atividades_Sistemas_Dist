import socket # Biblioteca de comunicação por rede
import hashlib # Biblioteca de criptografia hash
import threading # Biblioteca para processamento paralelo

# Define o host e a porta do servidor
HOST = '127.0.0.1' # Endereço IP do servidor
PORT = 55555 # Porta usada para a comunicação

# Cria o socket do cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um socket IPv4 usando o protocolo TCP
client.connect((HOST, PORT)) # Conecta-se ao servidor usando o endereço IP e a porta definidos acima

# Função para receber mensagens do servidor
def receive_messages():
    while True:
        # Recebe a mensagem criptografada do servidor
        encrypted_message = client.recv(1024)

        # Decodifica a mensagem criptografada usando o algoritmo SHA-256
        decrypted_message = hashlib.sha256(encrypted_message.decode().encode()).hexdigest()

        # Imprime a mensagem decodificada
        print(decrypted_message)

# Inicia uma thread para receber mensagens do servidor
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    # Lê a entrada do usuário
    message = input()

    # Criptografa a mensagem usando o algoritmo SHA-256
    encrypted_message = hashlib.sha256(message.encode()).hexdigest()

    # Envia a mensagem criptografada para o servidor
    client.send(encrypted_message.encode())

    # Se a mensagem do usuário for "bye", encerra o cliente
    if message == "bye":
        client.close()
        break

