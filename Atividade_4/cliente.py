import click
import grpc  # Importação do módulo grpc para comunicação gRPC
import my_service_pb2  # Importação do módulo gerado pelo protocol buffer
import my_service_pb2_grpc  # Importação do módulo gerado pelo protocol buffer para suporte a gRPC

@click.command()
@click.option('--server', default='localhost:50051', help='O endereço do servidor gRPC')
def execute_command(server):
    channel = grpc.insecure_channel(server)  # Cria um canal de comunicação gRPC não seguro
    stub = my_service_pb2_grpc.RemoteControlStub(channel)  # Cria um stub para a interface gRPC
    while True:
        command = input('Digite o comando que deseja executar: ')  # Solicita ao usuário para digitar o comando
        response = stub.ExecuteCommand(my_service_pb2.CommandRequest(command=command))  # Chama o método remoto ExecuteCommand e passa o comando digitado
        print(response.output)  # Exibe a saída recebida do servidor

if __name__ == '__main__':
    execute_command()  # Executa o comando principal quando o script é executado diretamente

