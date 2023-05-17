import socket
import psutil  # Importação do módulo psutil para obter informações do sistema
import matplotlib.pyplot as plt  # Importação do módulo matplotlib para plotar gráficos
import threading  # Importação do módulo threading para suporte a threads

HOST = ''
PORT = 5000

clients = []

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((HOST, PORT))  # Associa o servidor ao endereço de host e porta especificados
        print(f'Servidor escutando na porta {PORT}...')
        s.listen()  # Inicia a escuta por conexões
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = s.accept()  # Aceita uma nova conexão do cliente
        print(f'Conectado por {addr}')
        clients.append(client)  # Adiciona o cliente à lista de clientes conectados

        thread = threading.Thread(target=messagesTreatment, args=[client])  # Cria uma nova thread para tratar as mensagens do cliente
        thread.start()  # Inicia a thread

        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 3}")  # Exibe o número de conexões ativas

def messagesTreatment(client):
    while True:
        try:
            data = client.recv(1024)  # Recebe a mensagem do cliente
            print(f"Tamanho msg: {len(data)} bytes")
            if not data:
                deleteClient(client)  # Se a mensagem estiver vazia, remove o cliente da lista de clientes conectados e encerra o loop
                break
            msg = data.decode('utf-8')  # Decodifica a mensagem recebida
            msg_reversed = msg[::-1]  # Reverte a mensagem
            broadcast(msg_reversed, client)  # Envia a mensagem revertida para todos os clientes conectados, exceto o cliente atual

        except:
            deleteClient(client)  # Se ocorrer uma exceção, remove o cliente da lista de clientes conectados e encerra o loop
            break

def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg.encode('utf-8'))  # Envia a mensagem para todos os clientes conectados, exceto o cliente atual
            except:
                deleteClient(clientItem)  # Se ocorrer uma exceção ao enviar a mensagem, remove o cliente da lista de clientes conectados

def deleteClient(client):
    clients.remove(client)  # Remove o cliente da lista de clientes conectados

def plot_cpu_memory_network():
    # Cria figuras para os gráficos
    fig, ax = plt.subplots(3)

    # Configura o título e as legendas dos gráficos
    fig.suptitle('Utilização de CPU, memória e rede')
    ax[0].set_ylabel('CPU (%)')
    ax[1].set_ylabel('Memória (%)')
    ax[2].set_ylabel('Rede (MB/s)')

    # Lista vazia para armazenar os valores de CPU, memória e rede
    cpu_usage = []
    memory_usage = []
    network_usage = []

    # Loop para atualizar os valores dos gráficos a cada segundo
    while True:
        # Obtém os valores de uso da CPU, memória e rede do sistema operacional
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil
