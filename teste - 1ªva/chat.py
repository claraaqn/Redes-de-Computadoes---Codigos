from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Cria o socket
s = socket(AF_INET, SOCK_STREAM)
print('Tentando conectar ao servidor na porta 9002')

try:
    # Conecta ao servidor
    s.connect(('172.29.9.204', 9002))
    print("Conexão estabelecida!")
except ConnectionRefusedError:
    print("Falha ao conectar no servidor. Verifique o endereço e a porta.")
    exit(1)

# Envia o nick ao servidor
primeira_mensagem = input('Digite seu nick: ')
s.send(primeira_mensagem.encode())

# Recebe mensagens do servidor
def receber_mensagens(s):
    while True:
        try:
            mensagem = s.recv(1500).decode()
            if mensagem:
                print(f"{mensagem}")
            else:
                print("Servidor desconectado.")
                break
        except (ConnectionResetError, ConnectionAbortedError):
            print("Conexão encerrada pelo servidor.")
            break

# Envia mensagens para o servidor
def enviar_mensagens():
    while True:
        try:
            mensagem = input('Você: ')
            if mensagem:
                s.send(mensagem.encode())
        except (BrokenPipeError, ConnectionResetError):
            print("Conexão perdida. Não foi possível enviar a mensagem.")
            break

# Iniciar threads para envio e recebimento de mensagens
Thread(target=receber_mensagens, args=(s,), daemon=True).start()
Thread(target=enviar_mensagens, daemon=True).start()

# Mantém o programa rodando
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Encerrando conexão...")
    s.close()
