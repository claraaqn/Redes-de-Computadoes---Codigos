from socket import socket, AF_INET, SOCK_DGRAM

s = socket(AF_INET, SOCK_DGRAM)
print(f'Tentando conectar ao servidor na porta 9001')

# envia mensagem
while True:
    mensagem = input("Você: ")
    if mensagem == "esc":
        print('Cnexão encerrada')
        s.close()
        break
    else:
        s.sendto(mensagem.encode(), ('172.29.9.204', 9001))

# Recebe uma mensagem do servidor
    mensagem = s.recv(1500)
    if mensagem:
        print(f"Servidor: {mensagem.decode()}")
 