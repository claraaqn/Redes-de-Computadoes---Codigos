import socket
import struct
import random
import argparse

def consulta(dominio, tipo_registro):
    id = random.randint(0, 65535)  # ID aleatório para a consulta
    flags = 0x0100  # Solicitação padrão
    perguntas, resposta, autoritativas, adicionais = 1, 0, 0, 0
    cabecalho = struct.pack("!HHHHHH", id, flags, perguntas, resposta, autoritativas, adicionais)
    
    partes = dominio.split(".")
    rotulos = b"".join(struct.pack("!B", len(parte)) + parte.encode() for parte in partes) + b"\x00"
    tipos = {"A": 1, "AAAA": 28, "MX": 15}
    tipo = tipos.get(tipo_registro.upper(), 1)
    pergunta = struct.pack("!HH", tipo, 1)  # Classe 1 = IN (Internet)

    return id, cabecalho + rotulos + pergunta

def interprete_dns(resposta, id):
    resposta_id = struct.unpack("!H", resposta[:2])[0]
    if resposta_id != id:
        raise ValueError("IDs de transação não correspondem.")
    
    _, _, perguntas, respostas, _, _ = struct.unpack("!HHHHHH", resposta[:12])
    dados = resposta[12:]
    
    for _ in range(perguntas):
        while dados[0] != 0:
            dados = dados[dados[0] + 1:]
        dados = dados[5:]
    
    resultados = []
    for _ in range(respostas):
        if dados[0] & 0xC0 == 0xC0:
            dados = dados[2:]
        else:
            while dados[0] != 0:
                dados = dados[dados[0] + 1:]
            dados = dados[1:]
        
        tipo, classe, ttl, tamanho = struct.unpack("!HHIH", dados[:10])
        dados = dados[10:]
        
        if tipo == 1:  # Registro A (IPv4)
            valor = ".".join(map(str, dados[:4]))
            dados = dados[4:]
        elif tipo == 28:  # Registro AAAA (IPv6)
            valor = ":".join(f"{dados[i]:02x}{dados[i+1]:02x}" for i in range(0, 16, 2))
            dados = dados[16:]
        elif tipo == 15:  # Registro MX
            prioridade = struct.unpack("!H", dados[:2])[0]
            dados = dados[2:]
            nome_mx = []
            while dados[0] != 0:
                comprimento_label = dados[0]
                nome_mx.append(dados[1:1+comprimento_label].decode())
                dados = dados[1+comprimento_label:]
            dados = dados[1:]
            valor = f"{prioridade} {'.'.join(nome_mx)}"
        else:
            valor = f"Tipo desconhecido ({tipo})"
            dados = dados[tamanho:]
        
        resultados.append({
            "tipo": tipo,
            "classe": classe,
            "ttl": ttl,
            "comprimento": tamanho,
            "valor": valor,
        })
    
    return resultados

def consultar_dns(dominio, tipo_registro="A", servidor_dns=None):
    if servidor_dns is None:
        servidor_dns = "8.8.8.8"  # DNS padrão

    id, mensagem = consulta(dominio, tipo_registro)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(5)  # Timeout
        try:
            s.sendto(mensagem, (servidor_dns, 53))
            resposta, _ = s.recvfrom(4096)  # Buffer aumentado para respostas maiores
        except socket.timeout:
            raise TimeoutError("O servidor DNS não respondeu dentro do tempo limite.")

    return interprete_dns(resposta, id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente DNS")
    parser.add_argument("dominio", help="Nome do domínio a ser consultado")
    parser.add_argument("--tipo", default="A", help="Tipo de registro DNS (A, AAAA, MX)")
    parser.add_argument("--dns", help="Servidor DNS (padrão: automático)")
    args = parser.parse_args()
    
    try:
        resultados = consultar_dns(args.dominio, args.tipo, args.dns)
        print(f"Domínio: {args.dominio}")
        print(f"Tipo de registro: {args.tipo}")
        print("Resultados:")
        for res in resultados:
            print(f"  - Tipo: {res['tipo']}")
            print(f"    Classe: {res['classe']}")
            print(f"    TTL: {res['ttl']} segundos")
            print(f"    Comprimento: {res['comprimento']} bytes")
            print(f"    Valor: {res['valor']}")
    except TimeoutError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro: {e}")
