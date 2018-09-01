import socket
import threading
import sys

class Servidor:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # atributo sock
    # AF_INET -> ipv4
    # AF_SOCK_STREAM -> tcp
    conexoes = [] # atibuto que vai guardar as conexões

    def __init__(self): # __init__(self) -> construtor (em Python)
        self.sock.bind(('0.0.0.0', 8080))  # bind -> fala pra todo mundo que está aberta conexão em tal endereço e porta
        self.sock.listen(1) #self.atributo -> this.atributo


    def handler(self, conexao, endereco): # quando usar metodo vai ter q passar duas coisas: conexao e endereco
        # serve pra receber mensagem pela rede e replicar pra todo mundo que tá conectado no servidor
        while True:
            dados = conexao.recv(1024) # só recebe 1024 bytes
            for c in self.conexoes: # para cada conexão em conexões
                c.send(dados)
            if not dados:
                print(str(endereco[0]) + ':' + str(endereco[1]) + "desconectou!")
                self.conexoes.remove(conexao)
                conexao.close()
                break


    def run(self):
        while True:
            conexao, endereco = self.sock.accept()
            threadConexao = threading.Thread(target=self.handler, args=(conexao,endereco))
            # pelo target eu indico que o metodo que vai ser executada na thread é o handler
            # eu tenho que passar os argumentos do metodo em args
            threadConexao.daemon = True
            # se eu não coloca isso não fecha o programa
            threadConexao.start()
            self.conexoes.append(conexao)
            print(str(endereco[0]) + ':' + str(endereco[1]) + "conectou!")


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendMsg(self):
        while True:
            self.sock.send(bytes(input(""), 'utf-8')) # converte em bytes para mandar pela rede


    def __init__(self, enderecoServidor):
        self.sock.connect((enderecoServidor, 8080))
        threadInput = threading.Thread(target=self.sendMsg)
        threadInput.daemon = True
        threadInput.start()

        while True:
            dados = self.sock.recv(1024)
            if not dados:
                break
            print(str(dados, 'utf-8'))


# ver se veio atributo junto com a chamada do programa
if (len(sys.argv) > 1): # se largura do que veio junto com o nome do arquivo for maior que 1
    client = Client(sys.argv[1]) # variável client recebe objeto do tipo Client com atributo (servidor)
else:
    server = Servidor()
    server.run()