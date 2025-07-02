import Pyro5.api
import os
import hashlib # serve pra usar a funcao de hash

Pyro5.config.SERIALIZER = 'marshal'
#---------------------conexao servidorer 1  - proxy----------------------
ip_servidor_name='192.168.3.106'
ns = Pyro5.api.locate_ns(host=ip_servidor_name) #localiza servidor de nomes
uri = ns.lookup("servidor1") # obtem localizacao objeto sistema arquivos
servidor1= Pyro5.api.Proxy(uri)
#---------------------conexao servidorer 2  - proxy----------------------
#ip_servidor2='192.168.3.106'
ns = Pyro5.api.locate_ns(host=ip_servidor_name) #localiza servidor de nomes
uri = ns.lookup("servidor2") # obtem localizacao objeto sistema arquivos
servidor2= Pyro5.api.Proxy(uri)
#---------------------conexao servidorer 3  - proxy----------------------
#ip_servidor3='192.168.3.106'
ns = Pyro5.api.locate_ns(host=ip_servidor_name) #localiza servidor de nomes
uri = ns.lookup("servidor3") # obtem localizacao objeto sistema arquivos
servidor3= Pyro5.api.Proxy(uri)
#---------------------conexao servidorer 4  - proxy----------------------
#ip_servidor3='192.168.3.106'
ns = Pyro5.api.locate_ns(host=ip_servidor_name) #localiza servidor de nomes
uri = ns.lookup("servidor4") # obtem localizacao objeto sistema arquivos
servidor4= Pyro5.api.Proxy(uri)
#-------------------conexao servidor metadados - proxy-----------
#ip_servidor_metadados='192.168.3.106'
ns=Pyro5.api.locate_ns(host=ip_servidor_name)
uri_metadados=ns.lookup("servidormetadados")
proxy_metadados=Pyro5.api.Proxy(uri_metadados)
#==========================variaveis_global===============================
quantidade_servidores=4 # valor quantidade de servidores que tenho rodando 
vetor_quantidade_memoria=[0]*quantidade_servidores # esse vetor serve para armazenar a quantidade de memoria em cada servidor cluster

numero_servidor={ # mapeia numero para servidor
    "1": servidor1,
    "2": servidor2,
    "3": servidor3,
    "4": servidor4
}

nomes_servidores=["servidor1","servidor2","servidor3","servidor4"]

#=-------------------------funcoes-----------------------------------
def dividir_em_blocos(caminho_arquivo,tamanho_bloco): # divide arquivo em blocos de tamanho "m" e retorna lista com os blocos
    blocos=[] #lista de blocos
    with open(caminho_arquivo,"rb") as f:
        while True:
            bloco=f.read(tamanho_bloco)
            if not bloco:
                break
            blocos.append(bloco)
    return blocos
#--------------------------------------------------------------------------------------
def proxy_servidor_pra_conexao(num):
    proxy_servidor=numero_servidor.get(str(num))
    if proxy_servidor :
        return proxy_servidor
    else:
        print("numero servidor nao encontrado")
        return None
#--------------------------------------------------------------------------------------------------    
def quantidade_memoria_servidores(vetor_status): # me retorna vetor com a quantidade de memoria em cada servidor
    for i in range(quantidade_servidores):
        if(vetor_status[i]==1):
            aux=proxy_servidor_pra_conexao(i+1)
            memoria_servidor=aux.quantidade_memoria()
            vetor_quantidade_memoria[i]=memoria_servidor
        
    return vetor_quantidade_memoria

#--------------------------------------------------------------------------------------------------
def hash_conteudo(conteudo_bytes, algoritmo="sha256"):
    hash_func = getattr(hashlib, algoritmo)()
    hash_func.update(conteudo_bytes)
    return hash_func.hexdigest()
#-------------------------------------------------------------------
def atualizar_proxys(ip_servidores, nomes_objetos):
    ns = Pyro5.api.locate_ns(host=ip_servidores)  # Exemplo usando o primeiro IP para NS
    proxies_novos = {}

    for i, nome in enumerate(nomes_objetos, start=1):
        uri = ns.lookup(nome)
        proxies_novos[str(i)] = Pyro5.api.Proxy(uri)

    global numero_servidor
    for proxy_antigo in numero_servidor.values():
        try:
            proxy_antigo._pyroRelease()
        except Exception:
            pass

    numero_servidor = proxies_novos
    return proxies_novos
#-------------------------------------------------------------------
def verificar_servidores_online():
    atualizar_proxys(ip_servidor_name, nomes_servidores)
    vetor_status=[0]*quantidade_servidores
    for i in range(quantidade_servidores):
        proxy =numero_servidor.get(str(i + 1))  # servidores são "1", "2", "3", ...
        try:
            if proxy.ping() == "on":  # ping() precisa retornar "on"
                vetor_status[i] = 1
        except Exception:
            vetor_status[i] = 0  # já está assim por padrão

    return vetor_status
#-------------------------------------------------------------------
def balanceador_carga_servidor():
    vetor_status=verificar_servidores_online() # verifico quais servidores estao "on" - me retorna lista status servidores
    vetor_memoria=quantidade_memoria_servidores(vetor_status)
    print(vetor_memoria)
    valor_min=float("inf")
    indice_menor=None
    
    for i in range(quantidade_servidores):
        if(vetor_status[i]==1):
            if(vetor_memoria[i]<valor_min):
                valor_min=vetor_memoria[i]
                indice_menor=i

    return indice_menor
#-------------------------------------------------------------------
def replicacao(bloco,nome_arquivo,fat_replica):
    num_servidor_replica=[0]*fat_replica

    for i in range(fat_replica):
        name=nome_arquivo+("rep")+str(i+1) # ex : nome.txt2rep1
        num=balanceador_carga_servidor()
        aux=proxy_servidor_pra_conexao(num+1)
        num_servidor_replica[i]=num+1
        resposta = aux.upload(name,bloco,hash_conteudo(bloco))

        if(resposta !="ok"):
                print(f"erro ao enviar replica-1 bloco{i}")
                break
        
    return num_servidor_replica

#------------------------------------------------------------------
#diretorio_cliente='C:\\Users\mathe\OneDrive\Área de Trabalho\sistema distribuido\sistema arquivos\cliente'
diretorio_cliente='C:\\Users\Aluno\Documents\sd\cliente'

#-------------------------------------------------------------------------
def listar_arquivos():
    a=proxy_metadados.listar_nomes_arquivos()
    print(a)
#-------------------------------------------------------------------------
def baixar_servidor(nome,endereco_destino):
    informacao_arquivo=proxy_metadados.obter_localizacao_arquivo(nome)
    if(informacao_arquivo==None):
        print("\n nome nao encontrado servidor\n")
    else:
        mapa_blocos=informacao_arquivo['blocos']
        mapa_replicas=informacao_arquivo['replica']

        for informacao_bloco in mapa_blocos:
            num_bloco=informacao_bloco['bloco']
            id_servidor=informacao_bloco['id_servidor']
            servidores_ligados=verificar_servidores_online() # retorna quem esta on e off em um vetor

            if(servidores_ligados[id_servidor-1]==1):    # servidor esta on faz o download bloco normal
                aux=proxy_servidor_pra_conexao(id_servidor)
                fragmento=aux.receber_bloco_servidor(nome+str(num_bloco))

                if(fragmento==b"arquivo nao encontrado no servidor"):
                    print(f"\n nome : {nome+str(num_bloco)} - bloco :{num_bloco} nao encontrado servidor {id_servidor}")

                else :
                    endereco_completo=os.path.join(endereco_destino,nome) #endereco do arquivo baixado
                    with open(endereco_completo,"ab") as i: # "AB" escrita no final do arquivo,se fosse outro abria e apagava arquivo e escrevia
                            i.write(fragmento)
                    print(f"\n nome : {nome+str(num_bloco)} - bloco :{num_bloco} recebido e salvo")

            elif(servidores_ligados[id_servidor-1]==0):
                for informacao_replica in mapa_replicas: #procuro ate chegar bloco de replica que o servidor esta off do passo acima
                    if(informacao_replica['bloco']==num_bloco):
                        if(servidores_ligados[informacao_replica['id_servidor_1']-1]==1):
                            id_servidor=informacao_replica['id_servidor_1']
                            aux=proxy_servidor_pra_conexao(id_servidor)
                            fragmento=aux.receber_bloco_servidor(nome+str(num_bloco)+"rep1")

                            if(fragmento==b"arquivo nao encontrado no servidor"):
                                print("\n bloco nao encontrado servidor")

                            else :
                                endereco_completo=os.path.join(endereco_destino,nome) #endereco do arquivo baixado
                                with open(endereco_completo,"ab") as i: # "AB" escrita no final do arquivo,se fosse outro abria e apagava arquivo e escrevia
                                    i.write(fragmento)
                                print(f"\n nome : {nome+str(num_bloco)+'rep1'} - bloco : {num_bloco} recebido e salvo")
        
                        elif(servidores_ligados[informacao_replica['id_servidor_2']-1]==1):
                            id_servidor=informacao_replica['id_servidor_2']
                            aux=proxy_servidor_pra_conexao(id_servidor)
                            fragmento=aux.receber_bloco_servidor(nome+str(num_bloco)+'rep2')

                            if(fragmento==b"arquivo nao encontrado no servidor"):
                                print("\n bloco nao encontrado servidor")

                            else :
                                endereco_completo=os.path.join(endereco_destino,nome) #endereco do arquivo baixado
                                with open(endereco_completo,"ab") as i: # "AB" escrita no final do arquivo,se fosse outro abria e apagava arquivo e escrevia
                                    i.write(fragmento)
                                print(f"\n nome : {nome+str(num_bloco)+'rep2'} - bloco :{num_bloco} recebido e salvo")
                            
                        else:
                            print("\nTodos os servidores de um bloco que as replicas estao, esta off, tente novamente a operacao")

            


#-------------------------------------------------------------------------
def upload_arquivo(nome,diretorio):
    endereco_arquivo=os.path.join(diretorio,nome) # monta endereco arquivo (diretorio + nome arquivo)(coloca as \ sem dar problema codigo)
    tam_bloco=1024*1024 #1MB

    blocos=dividir_em_blocos(endereco_arquivo,tam_bloco)
    lista_blocos=[]
    lista_replicas=[]

    for i,bloco in enumerate(blocos,start=1):
        name=nome+str(i)
        num=balanceador_carga_servidor()
        aux=proxy_servidor_pra_conexao(num+1)
        resposta = aux.upload(name,bloco,hash_conteudo(bloco))

        if(resposta !="ok"):
            print(f"erro ao enviar bloco{i}")
            break
        
        vet_replicacao=replicacao(bloco,name,2)
        #print("inidice replicacao\n")
        #print(vet_replicacao)

        lista_blocos.append({"bloco":i, "id_servidor":num+1})
        lista_replicas.append({"bloco": i,"id_servidor_1": vet_replicacao[0],"id_servidor_2": vet_replicacao[1]})
        
    resultado=proxy_metadados.atualizar_arquivo(nome,len(blocos),lista_blocos,lista_replicas) # atualiza metadados de uma vez com a tabela 

#-------------------------------------------------------------------------
def deletar_arquivo(nome):
    informacao_arquivo=proxy_metadados.obter_localizacao_arquivo(nome)

    if(informacao_arquivo==None):
        print("\nnome arquivo invalido\n") #arquivo nao encontrado - nome nao existe
    else:
        mapa_blocos = informacao_arquivo['blocos']
        replicas = informacao_arquivo['replica']

        for bloco in mapa_blocos: #deleta bloco principal
            num_bloco = bloco['bloco']
            id_servidor = bloco['id_servidor']
            nome_bloco = nome + str(num_bloco)

            try:
                servidor = proxy_servidor_pra_conexao(id_servidor)
                servidor.deletar_bloco(nome_bloco)
                print(f"Bloco {nome_bloco} deletado do servidor {id_servidor}")
            except:
                print(f"Erro ao deletar bloco {nome_bloco} do servidor {id_servidor}")


        for replica in replicas:
            num_bloco = replica['bloco']

            for i in range(1, 3):  # 1 e 2
                id_replica = replica[f"id_servidor_{i}"]
                nome_replica = nome + str(num_bloco) + "rep" + str(i)

                try:
                    servidor = proxy_servidor_pra_conexao(id_replica)
                    servidor.deletar_bloco(nome_replica)
                    print(f"Replica {nome_replica} deletada do servidor {id_replica}")
                except:
                    print(f"Erro ao deletar replica {nome_replica} do servidor {id_replica}")

        # Atualiza metadados
        resultado = proxy_metadados.deletar_arquivo(nome)
        print(resultado)

#---------------------------------------------------------------
def status_servidor():
    print("\nStatus dos servidores:", verificar_servidores_online())
    print("\nMemória dos servidores:", quantidade_memoria_servidores(verificar_servidores_online()))
