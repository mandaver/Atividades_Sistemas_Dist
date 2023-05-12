import grpc
import remote_control_pb2
import remote_control_pb2_grpc

def run():
    # Cria um canal gRPC para se comunicar com o servidor
    with grpc.insecure_channel("localhost:50051") as channel:
        # Cria um stub do serviço RemoteControl
        stub = remote_control_pb2_grpc.RemoteControlStub(channel)
        # Loop principal do cliente
        while True:
            # Lê o comando inserido pelo usuário
            command = input("Insira um comando para executar (ou 'exit' para sair): ")
            # Verifica se o usuário deseja sair
            if command == "exit":
                break
            # Envia o comando para o servidor e recebe a resposta
            response = stub.ExecuteCommand(remote_control_pb2.CommandRequest(command=command))
            # Exibe o resultado da execução do comando
            print(response.output)

if __name__ == "__main__":
    run()
