from datetime import datetime
from json import loads, dumps
from pprint import pprint
import socket
from threading import Thread, RLock
from database import Database

from  common.datawrapper import DataWrapper

class ThreadedServer(Thread):
    def __init__(self, server, host, port, timeout=60, callback=None, debug=False):
        self.server = server
        self.host = host
        self.port = port
        self.timeout = timeout
        self.callback = callback
        self.debug = debug
        Thread.__init__(self)

    # run by the Thread object
    def run(self):
        if self.debug:
            print(datetime.now())
            print('Iniciando servidor...', '\n')

        self.listen()

    def listen(self):
        # cria instancia do socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # host e porta - sem teste para multihomed
        self.sock.bind((self.host, self.port))
        if self.debug:
            print(datetime.now())
            print('SERVIDOR socket ativo', self.host, self.port, '\n')

        # inicia a escuta
        self.sock.listen(5)
        if self.debug:
            print(datetime.now())
            print('SERVIDOR aguardando clientes...', '\n')
        while True:
            # leotura dos dados do socket
            client, address = self.sock.accept()

            # chamada para timeout
            #todo fazer callback melhor
            client.settimeout(self.timeout)

            if self.debug:
                print(datetime.now())
                print('CLIENTE Connectado:', client, '\n')

            # Inicia thread com o socket suspenso
            Thread(
                target=self.listenToClient,
                args=(client, address, self.callback)
            ).start()

    def listenToClient(self, client, address, callback):
        size = 1024
        while True:
            try:
                # leitura dos dados do cliente
                data = client.recv(size).decode('utf-8')
                if data:
                    json = loads(data.rstrip('\0'))
                    if self.debug:
                        print(datetime.now())
                        print('CLIENT Data Received', client)
                        print('Data:')
                        pprint(json, width=1)
                        print('\n')

                    if callback is not None:
                        callback(self, client, address, json) #! calback com o Dict()/JSON

                else:
                    raise 'Client disconnected'

            except:
                if self.debug:
                    print(datetime.now())
                    print('CLIENT Disconnected:', client, '\n')
                client.close()
                return False


#exemplo
def some_callback(server, sockClient, address, data):
    print('Dado recebido', data)
    # enviar resposta ao cliente
    try:
        hostRequest = DataWrapper.loadFromJSON( data )
        response = loads(hostRequest.json)
        sockClient.send(response.encode('utf-8'))
    except Exception as e:
        print( e )



#!usar modulo apenas
#if __name__ == "__main__":
#    ThreadedServer('127.0.0.1', 8008, timeout=86400, callback=some_callback, debug=True).start()
