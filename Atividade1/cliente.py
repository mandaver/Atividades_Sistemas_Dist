import sys
import socket
import threading
import base64

HOST = 'localhost'  # Endereço IP ou nome do host do servidor
PORT = 5000  # Porta utilizada para a conexão

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um objeto de socket TCP/IP

    try:
        client.connect((HOST, PORT))  # Conecta ao servidor utilizando o endereço e a porta especificados
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')  # Exibe uma mensagem de erro se a conexão falhar

    print('\nConectado')

    thread1 = threading.Thread(target=receiveMessages, args=[client])  # Cria uma thread para receber mensagens do servidor
    thread2 = threading.Thread(target=sendMessages, args=[client])  # Cria uma thread para enviar mensagens para o servidor

    thread1.start()  # Inicia a thread de recebimento de mensagens
    thread2.start()  # Inicia a thread de envio de mensagens

def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048)  # Recebe uma mensagem do servidor
            if not msg:  # Se a mensagem estiver vazia, significa que a conexão foi encerrada
                break
            else:
                decoded_msg = base64.b64decode(msg).decode('ascii')  # Decodifica a mensagem recebida (codificada em base64) para texto
                sys.stdout.write('\033[K' + decoded_msg + '\r\n')  # Exibe a mensagem decodificada na tela
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')  # Exibe uma mensagem de erro se a conexão falhar
            print('Pressione <Enter> para continuar...')
            client.close()  # Fecha a conexão com o servidor
            break

def sendMessages(client):
    while True:
        try:
            message = input().encode('ascii')  # Aguarda a entrada do usuário e codifica a mensagem em ASCII
            if not message:  # Se a mensagem estiver vazia, significa que o usuário quer encerrar a conexão
                client.close()  # Fecha a conexão com o servidor
                break
            base64_bytes = base64.b64encode(message)  # Codifica a mensagem em base64
            client.sendall(base64_bytes)  # Envia a mensagem codificada para o servidor
        except:
            return

main()  # Executa a função principal para iniciar a execução do programa

