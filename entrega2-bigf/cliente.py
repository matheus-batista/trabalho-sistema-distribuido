import Pyro5.api
import os

Pyro5.config.SERIALIZER = 'marshal'

ip_servidor='192.168.68.102'
ns = Pyro5.api.locate_ns(host=ip_servidor) #localiza servidor de nomes
uri = ns.lookup("sistema_arquivos") # obtem localizacao objeto sistema arquivos
proxy = Pyro5.api.Proxy(uri)

diretorio_cliente='C:\\Users\mathe\OneDrive\Área de Trabalho\sistema distribuido\sistema arquivos\cliente'

print()
op=int(input("\n --------digite uma opcao: -------------\n 1-listar\n 2-baixar\n 3-upload\n 4-deletar\n 5-sair\n ")) 

while(op!=5):
    if(op==1): # comando pra listar arquivos diretorio fixo servidor
        print("\narquivos :",proxy.ls())
        
    elif(op==2): # comando pra baixar arquivos servidor
        nome=input("digite nome arquivo a ser copiado :\n")
        endereco_destino=input("digite endereco de destino :\n")
        retorno=proxy.copy(nome)

        if(retorno ==b"arquivo nao encontrado no servidor"):
             print("\n arquivo nao encontrado servidor")

        else :
            endereco_completo=os.path.join(endereco_destino,nome) #endereco do arquivo copiado
            with open(endereco_completo,"wb") as i:
                    i.write(retorno)
            print("\n arquivo revebido e salvo")

    elif(op==3): #comando pra fazer upload arquivos pro servidor
         nome=input("digite nome arquivo para upload:\n")
         diretorio=input("digite endereco da pasta onde esta arquivo:\n")
         endereco_arquivo=os.path.join(diretorio,nome) # monta endereco arquivo (diretorio + nome arquivo)(coloca as \ sem dar problema codigo)

         try:   # tratamento de exceccao 
            with open(endereco_arquivo,"rb") as i:
                arquivo_bytes=i.read()
            print(proxy.upload(nome,arquivo_bytes))
         
         except FileNotFoundError:
            print("\narquivo nao encontrado no caminho especificado")
         
         
         

    print()
    op=int(input("\n --------digite uma opcao: -------------\n 1-listar\n 2-baixar\n 3-upload\n 4-deletar\n 5-sair\n "))     