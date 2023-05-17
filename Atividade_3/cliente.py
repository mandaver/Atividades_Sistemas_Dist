import socket
import random
import threading  

HOST = 'localhost'
PORT = 5000

# Tamanhos das mensagens em bytes
tamanhos = [1, 512, 1024]

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')

    username = input('Usuário> ')
    print('\nConectado')

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()

def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break

def sendMessages(client, username):
    while True:
        try:
            tamanho = random.choice(tamanhos)
            msg = b'K' * tamanho  # cria uma mensagem com o caracter 'K' repetido n vezes
            client.send(f'<{username}> {msg}'.encode('utf-8'))
            if msg == "quit":
                return False
        except:
            return

main()

