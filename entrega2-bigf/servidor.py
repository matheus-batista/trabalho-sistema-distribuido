import Pyro5.api
import os # serve para manipular diretorios
import shutil # biblioteca server para copiar arquivos
import threading

Pyro5.config.SERIALIZER = 'marshal'

# python -m Pyro5.nameserver --host 192.168.68.102 # roda cmd pra criar servidor de nomes com ip maquina

diretorio='C:\\Users\mathe\OneDrive\Área de Trabalho\sistema distribuido\sistema arquivos\servidor' # diretorio fixo servidor
# 'C:\\Users\Aluno\Documents\computacao grafica'
ip_servidor='192.168.68.102'

@Pyro5.server.expose
class sistema_arquivos:
    def ls(self):
       arquivos=os.listdir(diretorio)# carrego todos arquivos aqui
       #lista_arquivos = "\n".join(arquivos) # uso para separar nomes com \n 
       return arquivos
     
    def copy(self,nome):
         endereco_arquivo=os.path.join(diretorio,nome) # monta endereco arquivo (diretorio + nome arquivo)(coloca as \ sem dar problema codigo)
         try:   # tratamento de exceccao 
            with open(endereco_arquivo,"rb") as i:
                arquivo_bytes=i.read()
            return arquivo_bytes
         
         except FileNotFoundError:
            return b"arquivo nao encontrado no servidor"
         
    def upload(self,nome_arquivo,arquivos_bytes):
        endereco_completo=os.path.join(diretorio,nome_arquivo) #endereco : diretorio_servidor + nome_arquivo
        with open(endereco_completo,"wb") as i: 
                    i.write(arquivos_bytes)
        return "arquivo recebido e salvo"
        


def iniciar_thread(): # serve pra criar varias thread, varios clientes conectado ao mesmo tempo
    daemon = Pyro5.api.Daemon(host=ip_servidor) # especificar ip aqui para fazer conexao com outro pc
    ns = Pyro5.api.locate_ns(host=ip_servidor) # encontra servidor de nomes automaticamente
    uri = daemon.register(sistema_arquivos) # registra classe no daemon
    ns.register("sistema_arquivos", uri) # registra objeto servidor de nomes
    daemon.requestLoop()

# cria e inicia servidor em uma thread separada
thread = threading.Thread(target=iniciar_thread)
thread.start()
print("Thread do servidor rodando...")