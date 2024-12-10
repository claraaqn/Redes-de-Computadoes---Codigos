from socket import socket, AF_INET, SOCK_STREAM

s = socket(AF_INET, SOCK_STREAM)
print(f'Tentando conectar ao servidor na porta 80900')

s.connect(('172.29.9.204', 9000))
print('conectado')

# fazer ipconfig para ver meu IP
# meu ip: 172.29.9.54

# envia mensagem
while True:
    mensagem = input("Você: ")
    if mensagem == "esc":
        print('Cnexão encerrada')
        s.close()
        break
    else:
        s.send(mensagem.encode())

# Recebe uma mensagem do servidor
    mensagem = s.recv(1500)
    if mensagem:
        print(f"Servidor: {mensagem.decode()}")
    # avisar que o servidor acabou com a conexão
    if mensagem == "esc":
        print("Servidor fechou a conexão")
        s.close()
        break

