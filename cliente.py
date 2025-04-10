# -*- coding: utf-8 -*-
import socket

# Criar o socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Definir o host e a porta
host = '192.168.68.105'  # IP do servidor
port = 12345         # Porta do servidor

# Conectar ao servidor
client_socket.connect((host, port))

num=0
while num!="5":
    print()
    num=str(input("\n --------digite uma opcao: -------------\n 1-listar\n 2-remover\n 3-copy\n 4-baixar\n 5-sair\n ")) 

    if(num=="1"): # listar diretorio
        client_socket.send(num.encode())# Enviar uma resposta ao servidor
        dados=client_socket.recv(1024).decode('utf-8')#RESPOSTA SERVIDOR
        print("\n --------------LISTAGEM ARQUIVOS DIRETORIO-------------\n")
        print(dados)

    elif(num=="2"): # remover arquivo diretorio
        client_socket.send(num.encode()) # Enviar uma resposta ao servidor
        nome=str(input("\n------digite nome arquivo a ser excluido :---------\n"))
        client_socket.send(nome.encode())#envia nome servidor
        print(client_socket.recv(1024).decode('utf-8'))#RESPOSTA SERVIDOR

    elif(num=="3"): # copia arquivo de uma pasta para outra
        client_socket.send(num.encode()) # Enviar uma resposta ao servidor
        nome=str(input("\n------digite nome arquivo a ser copiado :---------\n"))
        client_socket.send(nome.encode())#envia nome servidor
        nome2=str(input("\n------digite o diretorio aonde sera colocado a copia arquivo :---------\n"))
        client_socket.send(nome2.encode())#envia endereco pasta para servidor
        print(client_socket.recv(1024).decode('utf-8'))#RESPOSTA SERVIDOR

    elif(num=="4"):# baixa arquivo de uma pasta
        client_socket.send(num.encode()) # Enviar uma resposta ao servidor
        nome=str(input("\n------digite nome arquivo a ser copiado :---------\n"))
        client_socket.send(nome.encode())#envia nome servidor
        nome2=str(input("\n------digite o diretorio aonde sera colocado a copia arquivo :---------\n"))
        client_socket.send(nome2.encode())#envia endereco pasta para servidor
        print(client_socket.recv(1024).decode('utf-8'))#RESPOSTA SERVIDOR

    elif(num=="5"):
      # Enviar uma resposta ao servidor
        client_socket.send(num.encode())

    else:
        print("comando invalido digite novamente\n")





