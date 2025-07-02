import Pyro5.api
import os # serve para manipular diretorios
import shutil # biblioteca server para copiar arquivos
import threading
import hashlib # serve pra usar a funcao de hash

Pyro5.config.SERIALIZER = 'marshal'

# python -m Pyro5.nameserver --host 192.168.3.106 # roda cmd pra criar servidor de nomes com ip maquina

diretorio='C:\\Users\mathe\OneDrive\Área de Trabalho\sistema distribuido\sistema arquivos\servidor2' # diretorio fixo servidor
#diretorio='C:\\Users\Aluno\Documents\sd\servidor'
ip_servidor='192.168.3.106'

@Pyro5.server.expose
class sistema_arquivos:

    def ping(self): # verifica se o servidor esta "on"
        return "on"
    
    def ls(self):
       arquivos=os.listdir(diretorio)# carrego todos arquivos aqui
       #lista_arquivos = "\n".join(arquivos) # uso para separar nomes com \n 
       return arquivos
     
    def receber_bloco_servidor(self,nome):
         endereco_arquivo=os.path.join(diretorio,nome) # monta endereco arquivo (diretorio + nome arquivo)(coloca as \ sem dar problema codigo)
         try:   # tratamento de exceccao 
            with open(endereco_arquivo,"rb") as i:
                arquivo_bytes=i.read()
            return arquivo_bytes
         
         except FileNotFoundError:
            return b"arquivo nao encontrado no servidor"
         
    def upload(self,nome_arquivo,arquivos_bytes,valor_hash):
        valor=self.hash_conteudo(arquivos_bytes)
        if(valor==valor_hash):
            endereco_completo=os.path.join(diretorio,nome_arquivo) #endereco : diretorio_servidor + nome_arquivo
            with open(endereco_completo,"wb") as i: 
                    i.write(arquivos_bytes)
            return "ok"
        else :
            return "bloco nao possui integridade"
        
    def quantidade_memoria(self): # retorna quantidade de memoria servidor
        valor_total=0
         
        for nome_arquivo in os.listdir(diretorio):
              diretorio_nome=os.path.join(diretorio,nome_arquivo)
              tam_arquivo=os.path.getsize(diretorio_nome)
              valor_total=valor_total + tam_arquivo
        valor_total=valor_total/(1024*1024)
        return valor_total
    
    def hash_conteudo(self,conteudo_bytes, algoritmo="sha256"):
        hash_func = getattr(hashlib, algoritmo)()
        hash_func.update(conteudo_bytes)
        return hash_func.hexdigest()
    
    def deletar_bloco(self, nome_arquivo):
        caminho = os.path.join(diretorio, nome_arquivo)
        if os.path.exists(caminho):
            os.remove(caminho)
            return "ok"
        else:
            return "arquivo não encontrado"



def iniciar_thread(): # serve pra criar varias thread, varios clientes conectado ao mesmo tempo
    daemon = Pyro5.api.Daemon(host=ip_servidor) # especificar ip aqui para fazer conexao com outro pc
    ns = Pyro5.api.locate_ns(host=ip_servidor) # encontra servidor de nomes automaticamente
    uri = daemon.register(sistema_arquivos) # registra classe no daemon
    ns.register("servidor2", uri) # registra objeto servidor de nomes
    daemon.requestLoop()

# cria e inicia servidor em uma thread separada
thread = threading.Thread(target=iniciar_thread)
thread.start()
print("Thread do servidor rodando...")


# para ser distribuido cada servidor.py precisa :
# ns.register("sistema_arquivos_n", uri) n=1,2,3,4... nome unico por maquina