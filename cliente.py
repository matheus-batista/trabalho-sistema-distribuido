import Pyro5.api

ns = Pyro5.api.locate_ns() #localiza servidor de nomes
uri = ns.lookup("calculadora") # obtem localizacao objeto calculadora
proxy = Pyro5.api.Proxy(uri)

op=int(input("digite a opcao\n"))
while(op!=7):
    if(op==1):
        a=int(input("digite primeiro numero :\n"))
        b=int(input("digite segundo numero :\n"))
        print("\nresultado :",proxy.soma(a,b))
    elif(op==2):
        a=int(input("digite primeiro numero :\n"))
        b=int(input("digite segundo numero :\n"))
        print("\nresultado :",proxy.subtracao(a,b))
    elif(op==3):
        a=int(input("digite primeiro numero :\n"))
        b=int(input("digite segundo numero :\n"))
        print("\nresultado :",proxy.multiplicacao(a,b))
    elif(op==4):
        a=int(input("digite primeiro numero :\n"))
        b=int(input("digite segundo numero :\n"))
        print("\nresultado :",proxy.divisao(a,b))
    elif(op==5):
        a=int(input("digite primeiro numero :\n"))
        print("\nresultado :",proxy.raiz(a))
    elif(op==6):
        a=int(input("digite primeiro numero :\n"))
        b=int(input("digite segundo numero :\n"))
        print("\nresultado :",proxy.exponenciacao(a,b))

    op=int(input("digite a opcao\n"))
