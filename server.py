import socket
import os # manipular diretorio 
import shutil # biblioteca server para copiar arquivos

# Criar o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Definir o host e a porta
host = '192.168.68.103'  # IP local
port = 12345         # Porta do servidor

# Vincular o socket ao endereço e porta
server_socket.bind((host, port))

# Colocar o servidor em modo de escuta
server_socket.listen(1)
print(f"Servidor ouvindo em {host}:{port}...")

# Aguardar a conexão do cliente
client_socket, client_address = server_socket.accept()
print(f"Conexão estabelecida com {client_address}")

# Enviar uma mensagem para o cliente
#client_socket.send("ola cliente".encode())
num="0"

diretorio='C:\\Users\mathe\OneDrive\Área de Trabalho\sistema distribuido'
while num!="5":

    num = client_socket.recv(1024).decode() # recebe numero opcao lado cliente # Recebe uma mensagem do cliente

    if(num=="1"): #listar diretorio 
    
       arquivos=os.listdir(diretorio)# carrego todos arquivos aqui
       lista_arquivos = "\n".join(arquivos) # uso para separar nomes com \n 
       client_socket.send(lista_arquivos.encode()) # mando mensagem pro cliente com os arquivos no diretorio 

    elif(num=="2"): # remover arquivo diretorio
        nome_arquivo= client_socket.recv(1024).decode() # recebe nome arquivo lado cliente
        endereco_arquivo=os.path.join(diretorio,nome_arquivo)
        mensagem=""
        try:   # tratamento de exceccao 
            os.remove(endereco_arquivo)
            mensagem="arquivo removido com sucesso\n"
        except FileNotFoundError:
            mensagem="arquivo nao encontrado diretorio\n"

        client_socket.send(mensagem.encode()) # mensagem pro cliente pra confirmar se excluiu ou nao

    elif(num=="3"): # copia arquivo de um lugar para outro especificado
        nome_arquivo= client_socket.recv(1024).decode() # recebe nome arquivo lado cliente
        endereco_arquivo=os.path.join(diretorio,nome_arquivo) # monta endereco arquivo (diretorio + nome arquivo)(coloca as \ sem dar problema codigo)
        endereco_pasta_destino= client_socket.recv(1024).decode() # recebe cliente endereco da pasta de destino arquivo copiado
        try:   # tratamento de exceccao 
            shutil.copy(endereco_arquivo,endereco_pasta_destino)
            mensagem="arquivo copiado com sucesso\n"
        except FileNotFoundError:
            mensagem="arquivo nao encontrado diretorio\n"
        
        client_socket.send(mensagem.encode()) # mensagem pro cliente pra confirmar se fez copia ou nao

      
    elif(num=="4"): # funcao de baixar arquivo, fiz semelhante a num==3
        nome_arquivo= client_socket.recv(1024).decode() # recebe nome arquivo lado cliente
        endereco_arquivo=os.path.join(diretorio,nome_arquivo) # monta endereco arquivo (diretorio + nome arquivo)(coloca as \ sem dar problema codigo)
        endereco_pasta_destino= client_socket.recv(1024).decode() # recebe cliente endereco da pasta de destino arquivo copiado
        try:   # tratamento de exceccao 
            shutil.copy(endereco_arquivo,endereco_pasta_destino)
            mensagem="arquivo copiado com sucesso\n"
        except FileNotFoundError:
            mensagem="arquivo nao encontrado diretorio\n"
        
        client_socket.send(mensagem.encode()) # mensagem pro cliente pra confirmar se fez copia ou nao
       
       
    elif(num=="5"):
        # Fechar a conexão
        client_socket.close()
        server_socket.close()


