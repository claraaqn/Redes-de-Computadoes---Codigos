from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

clientes_conectados = []

# Worker para gerenciar a comunicação com o cliente
def conexao_cliente(cliente_socket, endereco_cliente):
    print(f'Conexão estabelecida com {endereco_cliente}')
    clientes_conectados.append(cliente_socket)

    while True:
        try:
            # Receber uma mensagem do cliente
            mensagem = cliente_socket.recv(1500)
            print(f"Mensagem de {endereco_cliente}: {mensagem.decode()}")
            # encerrar conexão
            if not mensagem or mensagem.decode() == "esc":
                print(f"{endereco_cliente} desconectou.")
                cliente_socket.close()
                break
            
            # responder cleinte por vez
            for outro_cliente in clientes_conectados:
                    try:
                        print(f"Respondendo: {endereco_cliente}")
                        mensagem = input("Servidor: ")
                        if mensagem == b"esc":
                            print('Cnexão encerrada')
                            cliente_socket.close()
                            break
                        else:
                            cliente_socket.send(mensagem.encode())
                    except ConnectionResetError:
                        outro_cliente.close()
                        clientes_conectados.remove(outro_cliente)
        except ConnectionResetError:
            break

    # Remover o cliente desconectado da lista e fechar o socket
    clientes_conectados.remove(cliente_socket)
    cliente_socket.close()
    print(f"Conexão com {endereco_cliente} encerrada")

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
    Thread(target=conexao_cliente, args=(cliente_socket, endereco_cliente)).start()
