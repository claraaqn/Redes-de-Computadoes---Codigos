from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Configuração do socket do cliente
s = socket(AF_INET, SOCK_STREAM)
print(f'Tentando conectar ao servidor na porta 8000')
s.connect(('127.0.0.1', 8000))

# Função para receber mensagens do servidor
def receber_mensagens(s):
    while True:
        try:
            mensagem = s.recv(1500)
            if mensagem:
                print(f"Mensagem do servidor: {mensagem.decode()}")
            if not mensagem or mensagem.decode() == "esc":
                print("Servidor fechou a conexão")
                s.close()
                break
        except ConnectionAbortedError:
            break
        except OSError:
            break

def enviar_menssagens(s):
    while True:
        mensagem = input("Você: ")
        if not mensagem or mensagem.encode() == "esc":
            print('Conexão encerrada')
            s.send(mensagem.encode())
            s.close()
            break
        else:
            s.send(mensagem.encode())

# Iniciar a thread para receber mensagens
Thread(target=receber_mensagens, args=(s,)).start()
Thread(target=enviar_menssagens, args=(s,)).start()
