import Pyro5.api
import threading
import json
import os

ip_servidor_metadados='192.168.3.106'

@Pyro5.api.expose # tudo que esta dentro da classe pode ser chamado na rede 

class servidormetadados:
    def listar_nomes_arquivos(self):
        return list(self.tabela.keys())

    def __init__(self): # inicia servidor e carrega dados
        self.arquivo_metadados = "metadados.json"
        self.carregar_metadados()

    def carregar_metadados(self):
        if os.path.exists(self.arquivo_metadados):
                with open(self.arquivo_metadados, "r") as f:
                        self.tabela = json.load(f)
        else:
                self.tabela = {}

    def salvar_metadados(self):
        with open(self.arquivo_metadados, "w") as f:
                json.dump(self.tabela, f)

    def obter_localizacao_arquivo(self, nome_arquivo):
        return self.tabela.get(nome_arquivo, None)

    def atualizar_arquivo(self, nome_arquivo, total_blocos, blocos,replica):
        self.tabela[nome_arquivo] = {
                "total_blocos": total_blocos,
                "blocos": blocos,
                "replica":replica
        }
        self.salvar_metadados()
        return "Metadados atualizados"

    def deletar_arquivo(self, nome_arquivo):
        if nome_arquivo in self.tabela:
                del self.tabela[nome_arquivo]
                self.salvar_metadados()
                return "Arquivo deletado dos metadados"
        else:
                return "Arquivo não encontrado nos metadados"


def iniciar_servidor():
        daemon = Pyro5.api.Daemon(host=(ip_servidor_metadados))
        ns = Pyro5.api.locate_ns(host=(ip_servidor_metadados))
        uri = daemon.register(servidormetadados)
        ns.register("servidormetadados", uri)
        print("Servidor de metadados rodando.")
        daemon.requestLoop()

if __name__ == "__main__":
    iniciar_servidor()
    
