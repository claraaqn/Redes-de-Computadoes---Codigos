from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import tkinter as tk

# Cria o socket
s = socket(AF_INET, SOCK_STREAM)
print(f'Tentando conectar ao servidor na porta 8000')

# Conecta ao servidor
s.connect(('127.0.0.1', 8000))

# Recebe uma mensagem do servidor
def receber_mensagens(s):
    while True:
        mensagem = s.recv(1500).decode()
        atualizar_interface(mensagem)

# envia mensagem
def enviar_menssagens():
    mensagem = caixa_texto.get()
    if mensagem:
        s.send(mensagem.encode())
        caixa_texto.delete(0, tk.END)
        
# muda a interface
def atualizar_interface(mensagem):
    mensagens_box.insert(tk.END, mensagem + "\n")
    mensagens_box.see(tk.END)  # Rola a barra de rolagem para o final

# acaba a conexão
def desconectar():
    s.close()
    print("Desconectado do servidor.")
    janela.quit()

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
