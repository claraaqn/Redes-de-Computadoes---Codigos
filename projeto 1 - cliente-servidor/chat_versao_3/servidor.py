from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

clientes_conectados = []

# Worker para gerenciar a comunicação com o cliente
def gerenciar_cliente(cliente_socket, endereco_cliente):
    print(f'Conexão estabelecida com {endereco_cliente}')
    clientes_conectados.append(cliente_socket)

    while True:
        try:
            # Receber uma mensagem do cliente
            mensagem = cliente_socket.recv(1500)
            if not mensagem: # ajeitar isso aq
                break
                
            print(f"Mensagem recebida de {endereco_cliente}: {mensagem.decode()}")

            # Envia a mensagem para todos os outros clientes conectados
            for outro_cliente in clientes_conectados:
                if outro_cliente != cliente_socket:
                    outro_cliente.send(mensagem)
        
        except ConnectionResetError:
            print(f"Conexão com {endereco_cliente} foi encerrada inesperadamente.")
            break

# Cria o socket servidor
server_socket = socket(AF_INET, SOCK_STREAM)

# Liga o servidor ao endereço IP e porta
server_socket.bind(('127.0.0.1', 8000))

# Coloca o servidor em modo de escuta
server_socket.listen()

print('Aguardando por novas requisiçõse na porta 8000')

# Ficar esperando por novas conexões de diferentes clientes
while True:
    # Aceita a conexão
    cliente_socket, endereco_cliente = server_socket.accept()
    Thread(target=gerenciar_cliente, args=(cliente_socket, endereco_cliente)).start()
    