from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import tkinter as tk

# Cria o socket
s = socket(AF_INET, SOCK_STREAM)
print(f'Tentando conectar ao servidor na porta 8000')

# Conecta ao servidor
s.connect(('127.0.0.1', 8000))

def receber_mensagens(s):
    while True:
        mensagem = s.recv(1024).decode()
        atualizar_interface(mensagem)

def enviar_mensagens():
    mensagem = caixa_texto.get()
    if mensagem:
        s.send(mensagem.encode())
        caixa_texto.delete(0, tk.END)
            
def atualizar_interface(mensagem):
    area_mensagens.insert(tk.END, mensagem + "\n")
    area_mensagens.see(tk.END)  # Rola a barra de rolagem para o final

def desconectar():
    s.close()
    print("Desconectado do servidor.")
    janela.quit()


janela = tk.Tk()
janela.title("Chat - Versão 3")

area_mensagens = tk.Text(janela)
area_mensagens.pack()
caixa_texto = tk.Entry(janela)
caixa_texto.pack()
botao_enviar = tk.Button(janela, text="Enviar", command=enviar_mensagens)
botao_enviar.pack()
botao_desconectar = tk.Button(janela, text="Desconectar", command=desconectar)
botao_desconectar.pack()

# thread para receber e enviar mensagens
Thread(target=receber_mensagens, args=(s,)).start()

janela.mainloop()
