from socket import socket, AF_INET, SOCK_STREAM
from time import sleep

# Cria o socket
s = socket(AF_INET, SOCK_STREAM)
print(f'Tentando conectar ao servidor na porta 8000')

# Conecta ao servidor
s.connect(('127.0.0.1', 8000))

# Recebe uma mensagem do servidor
while True:
    mensagem = s.recv(1500)
    if mensagem:
        print(f"Servidor: {mensagem.decode()}")
    # avisar que o servidor acabou com a conexão
    if mensagem == b"esc":
        print("Servidor fechou a conexão")
        s.close()
        break

# envia mensagem
    mensagem = input("Você: ")
    # vai ter uma forma de quebrar a conexão
    if mensagem == b"esc":
        print('Cnexão encerrada')
        s.close()
        break
    else:
        s.send(mensagem.encode())


#pegar hora atual
# from datetime import datetime
# hora_atual = datetime.now().strftime('%H:%M:%S')

# while True:
#     # Envia uma mensagem para o servidor
#     s.send(f'Olá, servidor! A hora atual é {datetime.now().strftime('%H:%M:%S')}'.encode())
#     sleep(1)


# Fecha a conexão
# s.close()