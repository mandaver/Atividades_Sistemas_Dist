<h1> Atividade 4</h1>


>Objetivo 
+ Permitir que o cliente envie comandos em formato de string para o servidor, para ele executar os comandos em uma máquina linux e retornar o resultado para o cliente+ Exemplo: ao enviar a string "Hello World!!!" ao servidor a mensagem "!!!dlroW olleH" deve ser respondida ao cliente.


> Recursos Utilizados 
+ Máquina virtual: Ubunto 22.04
+ Python 3

> Bibliotecas utilizadas 
+ subprocess
+ grpc
+ click

> Comandos para execução
+ python3 -m grpc_tools.protc -I./ --python_out=. --grpc_python_out=. my_service.proto
+ python3 server_grpc.py
+ python3 cliente_grpc.py
