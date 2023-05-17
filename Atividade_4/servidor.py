import subprocess  # Importação do módulo subprocess para execução de comandos externos
import grpc  # Importação do módulo grpc para comunicação gRPC
import my_service_pb2  # Importação do módulo gerado pelo protocol buffer
import my_service_pb2_grpc  # Importação do módulo gerado pelo protocol buffer para suporte a gRPC
from concurrent import futures  # Importação do módulo concurrent.futures para suporte a execução assíncrona
import logging

# Configurações do logger
logging.basicConfig(filename='server.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class RemoteControlServicer(my_service_pb2_grpc.RemoteControlServicer):
    def ExecuteCommand(self, request, context):
        command = request.command
        logging.info(f'Command received: {command}')
        output = subprocess.check_output(request.command, shell=True)  # Executa o comando recebido utilizando o módulo subprocess
        return my_service_pb2.CommandResponse(output=output.decode('utf-8'))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # Cria um servidor gRPC com suporte a execução assíncrona
    my_service_pb2_grpc.add_RemoteControlServicer_to_server(RemoteControlServicer(), server)  # Registra o servicer no servidor
    server.add_insecure_port('[::]:50051')  # Configura a porta para o servidor aceitar conexões não seguras
    server.start()  # Inicia o servidor
    server.wait_for_termination()  # Aguarda o encerramento do servidor

if __name__ == '__main__':
    serve()  # Inicia o servidor quando o script é executado diretamente
