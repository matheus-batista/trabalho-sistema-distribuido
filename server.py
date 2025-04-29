import math
import Pyro5.api

# python -m Pyro5.nameserver # roda cmd pra criar servidor de nomes

@Pyro5.server.expose
class calculadora:
    def soma(self,a,b):
        return (a+b)
    def subtracao(self,a,b):
        return (a-b)
    def multiplicacao(self,a,b):
        return (a*b)
    def divisao(self,a,b):
        return (a/b)
    def raiz(self,a):
        return (math.sqrt(a))
    def exponenciacao(self,a,b):
        return (a**b)

daemon = Pyro5.api.Daemon()
ns = Pyro5.api.locate_ns() # encontra servidor de nomes automaticamente
uri = daemon.register(calculadora) # registra classe no daemon
ns.register("calculadora", uri) # registra objeto servidor de nomes

print("URI do servidor: ",uri)
daemon.requestLoop()

