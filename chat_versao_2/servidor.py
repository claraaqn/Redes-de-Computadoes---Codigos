from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import tkinter as tk

clientes_conectados = {}

# Worker para gerenciar a comunicação com o cliente
def gerenciar_cliente(cliente_socket, endereco_cliente):
    atualizar_interface(f"Conexão estabelecida com {endereco_cliente}")
    clientes_conectados[endereco_cliente] = cliente_socket
    atualizar_menu_clientes()
        
    while True:
        try:
            mensagem = cliente_socket.recv(1500)
            atualizar_interface(f"{endereco_cliente}: {mensagem.decode()}")
        except ConnectionResetError:
            atualizar_interface(f"Conexão com {endereco_cliente} foi interrompida.")
            del clientes_conectados[endereco_cliente]
            cliente_socket.close()
            atualizar_menu_clientes()
            break
        
# envia mensagem
def enviar_mensagens():
    destinatario = cliente_selecionado.get()
    mensagem = caixa_texto.get()
    if destinatario in clientes_conectados and mensagem:
        clientes_conectados[destinatario].send(mensagem.encode())
        caixa_texto.config(state="normal")
        caixa_texto.insert(tk.END, f"Servidor para {destinatario}: {mensagem}\n")
        caixa_texto.config(state="disabled")
        caixa_texto.see(tk.END)
        caixa_texto.delete(0, tk.END)
    else:
        print("Cliente não selecionado ou mensagem vazia.")
                
# muda a interface
def atualizar_interface(mensagem):
    caixa_texto.config(state="normal")
    caixa_texto.insert(tk.END, mensagem + "\n")
    caixa_texto.config(state="disabled")
    caixa_texto.see(tk.END)

# começa o servidor
def iniciar_servidor():
    # Cria o socket servidor
    server_socket = socket(AF_INET, SOCK_STREAM)

    # Liga o servidor ao endereço IP e porta
    server_socket.bind(('127.0.0.1', 8000))

    # Coloca o servidor em modo de escuta
    server_socket.listen()

    print('Aguardando por novas requisiçõse na porta 8000')

    while True:
        cliente_socket, endereco_cliente = server_socket.accept()
        Thread(target=gerenciar_cliente, args=(cliente_socket, endereco_cliente)).start()

# muda a seleção do cliente
def atualizar_menu_clientes():
    menu = cliente_menu["menu"]
    menu.delete(0, "end")
    for endereco in clientes_conectados.keys():
        menu.add_command(label=endereco, command=tk._setit(cliente_selecionado, endereco))


# elementos da interface
janela = tk.Tk()
janela.title("Servidor de Chat - Versão 2")
janela.geometry("500x500")
caixa_texto = tk.Text(janela, state="disabled", wrap="word")
caixa_texto.pack(padx=10, pady=10, expand=True, fill="both")
cliente_selecionado = tk.StringVar(janela)
cliente_selecionado.set("Escolha um cliente")
cliente_menu = tk.OptionMenu(janela, cliente_selecionado, "Escolha um cliente")
cliente_menu.pack(padx=10, pady=5)
entrada_mensagem = tk.Entry(janela, width=50)
entrada_mensagem.pack(padx=10, pady=5)
enviar_button = tk.Button(janela, text="Enviar", command=enviar_mensagens)
enviar_button.pack(pady=5)

# iniciar o servidor
Thread(target=iniciar_servidor).start()

janela.mainloop()