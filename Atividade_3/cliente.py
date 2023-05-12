import socket  # Importa o módulo socket para utilizar comunicação em rede
import threading  # Importa o módulo threading para enviar múltiplas requisições

def send_message(sock, message):
    # Função que envia uma mensagem para o servidor e imprime a resposta recebida
    sock.sendall(message.encode())  # Codifica e envia a mensagem para o servidor
    response = sock.recv(1024)  # Recebe a resposta do servidor
    print(f"Resposta do servidor: {response.decode()}")  # Imprime a resposta do servidor

def start_client(host, port, num_threads, message):
    # Função que inicia o cliente
    threads = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))  # Conecta-se ao servidor no endereço e porta especificados
        for i in range(num_threads):
            t = threading.Thread(target=send_message, args=(s, message))  # Cria uma nova thread para enviar a mensagem para o servidor
            t.start()  # Inicia a thread
            threads.append(t)  # Adiciona a thread à lista de threads criadas
        for t in threads:
            t.join()  #

