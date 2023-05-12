import socket
import threading

def handle_client(conn, addr):
    print(f"Nova conexão de {addr[0]}:{addr[1]}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        data = data.decode()[::-1]  # Inverte a string recebida
        conn.sendall(data.encode())
    print(f"Conexão encerrada com {addr[0]}:{addr[1]}")
    conn.close()

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor iniciado em {host}:{port}")
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8000
    start_server(HOST, PORT)
