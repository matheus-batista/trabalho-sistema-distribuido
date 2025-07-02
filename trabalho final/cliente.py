import appmanager
import Pyro5.api
import os
import hashlib
import time

print()
op=int(input("\n --------digite uma opcao: -------------\n 1-listar\n 2-baixar\n 3-upload\n 4-deletar\n 5-status servidor\n 6-sair\n ")) 

while(op!=6):
    if(op==1): # comando pra listar arquivos que estao no servidor
        appmanager.listar_arquivos()
        
    elif(op==2): # comando pra baixar arquivos servidor
        nome=input("digite nome arquivo a ser copiado :\n")
        endereco_destino=input("digite endereco de destino :\n")
        inicio = time.perf_counter()
        appmanager.baixar_servidor(nome,endereco_destino)
        fim = time.perf_counter()
        latencia_ms = (fim - inicio) * 1000
        print(f"tempo: {latencia_ms:.2f} ms")

    elif(op==3): #comando pra fazer upload arquivos pro servidor
        nome=input("digite nome arquivo para upload:\n")
        diretorio=input("digite endereco da pasta onde esta arquivo:\n")
        appmanager.upload_arquivo(nome,diretorio)
        
    elif(op==4): # deletar arquivo
        nome=input("digite nome arquivo para deletar:\n")
        appmanager.deletar_arquivo(nome)
           
    elif(op==5): # status servidor
        appmanager.status_servidor()

    print()
    op=int(input("\n --------digite uma opcao: -------------\n 1-listar\n 2-baixar\n 3-upload\n 4-deletar\n 5-status servidor\n 6-sair\n "))     
