from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import tkinter as tk
import os

# Cria o socket
s = socket(AF_INET, SOCK_STREAM)
print(f'Tentando conectar ao servidor na porta 8000')

# Conecta ao servidor
s.connect(('127.0.0.1', 8000))

# Recebe uma mensagem do servidor
def receber_mensagens(s):
    while True:
        try:
            mensagem = s.recv(1500).decode()
            atualizar_interface(f"Servidor: {mensagem}")
        except (ConnectionResetError, ConnectionAbortedError):
            atualizar_interface("Conexão encerrada.")
            break

# envia mensagem
def enviar_menssagens():
    mensagem = caixa_texto.get()
    if mensagem:
        s.send(mensagem.encode())
        atualizar_interface(f"Você: {mensagem}")
        caixa_texto.delete(0, tk.END)
        
# muda a interface
def atualizar_interface(mensagem):
    mensagens_box.config(state="normal")
    mensagens_box.insert(tk.END, mensagem + "\n")
    mensagens_box.config(state="disabled")
    mensagens_box.see(tk.END)  # Rola a barra de rolagem para o final

# acaba a conexão
def desconectar():
    s.close()
    print("Desconectado do servidor.")
    janela.quit()
    os._exit(0)

# elementos da interface
janela = tk.Tk()
janela.title("Cleinte Chat - Versão 2")
janela.geometry("500x500")
mensagens_box = tk.Text(janela, state="disabled", wrap="word")
mensagens_box.pack(padx=10, pady=10, expand=True, fill="both")
caixa_texto = tk.Entry(janela, width=50)
caixa_texto.pack(padx=10, pady=5)
botao_enviar = tk.Button(janela, text="Enviar", command=enviar_menssagens)
botao_enviar.pack(pady=5)
botao_desconectar = tk.Button(janela, text="Desconectar", command=desconectar)
botao_desconectar.pack()

# Iniciar a thread para receber mensagens
Thread(target=receber_mensagens, args=(s,)).start()

janela.mainloop()
