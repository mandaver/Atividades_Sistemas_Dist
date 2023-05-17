import socket
import threading
import base64

HOST = ''  # Endereço IP ou nome do host em que o servidor será executado
PORT = 5000  # Porta utilizada pelo servidor

clients = []  # Lista para armazenar os clientes conectados

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um objeto de socket TCP/IP

    try:
        s.bind((HOST, PORT))  # Associa o socket ao endereço e à porta especificados
        print(f'Servidor escutando na porta {PORT}...')
        s.listen()  # Inicia a escuta por conexões entrantes
    except:
        return print('\nNão foi possível iniciar o servidor!\n')  # Exibe uma mensagem de erro se ocorrer um problema ao iniciar o servidor

    while True:
        client, addr = s.accept()  # Aceita uma conexão de um cliente
        print(f'Conectado por {addr}')
        clients.append(client)  # Adiciona o cliente à lista de clientes conectados

        thread = threading.Thread(target=messagesTreatment, args=[client])  # Cria uma thread para tratar as mensagens do cliente
        thread.start()  # Inicia a thread

def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(2048)  # Recebe uma mensagem do cliente
            if not msg:  # Se a mensagem estiver vazia, significa que a conexão foi encerrada pelo cliente
                deleteClient(client)  # Remove o cliente da lista de clientes conectados
                break
            decoded_message = client.getpeername()[0] + ': ' + base64.b64decode(msg).decode('ascii')  # Decodifica a mensagem recebida (codificada em base64) para texto
            encoded_message = base64.b64encode(decoded_message.encode('ascii'))  # Codifica a mensagem em base64
            print(encoded_message)  # Exibe a mensagem codificada (somente para depuração)
            print(decoded_message)  # Exibe a mensagem decodificada (somente para depuração)
            broadcast(encoded_message, client)  # Envia a mensagem para todos os outros clientes conectados
        except:
            deleteClient(client)  # Remove o cliente da lista de clientes conectados em caso de erro
            break

def broadcast(msg, sender_client):
    for clientItem in clients:
        if clientItem != sender_client:  # Envia a mensagem para todos os clientes, exceto o remetente original
            try:
                clientItem.send(msg)  # Envia a mensagem codificada para o cliente
            except:
                deleteClient(clientItem)  # Remove o cliente da lista de clientes conectados em caso de erro ao enviar a mensagem

def deleteClient(client):
    clients.remove(client)  # Remove o cliente da lista de clientes conectados

main()  # Executa a função principal para iniciar o servidor
