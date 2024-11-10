from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Cria o socket
s = socket(AF_INET, SOCK_STREAM)
print(f'Tentando conectar ao servidor na porta 8000')

# Conecta ao servidor
s.connect(('127.0.0.1', 8000))

def receber_mensagens(s):
    while True:
        mensagem = s.recv(1500)
        if mensagem:
            print(f"Fulano: {mensagem.decode()}")
        if mensagem.decode() == "esc":
            print("conexão fechada")
            s.close()
            break

def enviar_mensagens(s):
    while True:
        mensagem = input("Você: ")
        if mensagem == "esc":
            print('Conexão encerrada')
            s.send(mensagem.encode())
            s.close()
            break
        else:
            s.send(mensagem.encode())

# thread para receber e enviar mensagens
Thread(target=receber_mensagens, args=(s,)).start()
Thread(target=enviar_mensagens, args=(s,)).start()

