from database import Database
import os
import time
from serverconfig import ServerConfig
import common.constants as CONSTANTS
from common.datawrapper import DataWrapper
from server import ThreadedServer
from threading import Thread, RLock

import json

ThreadLock = RLock()

class Server():

    #construtor
    def __init__(self):
        super().__init__()
        self._cfg = None
        self.__db = None

    @property
    def db(self):
        return self.__db

    @property
    def config(self):
        return self._cfg

    def startDatabase(self):
        self.__db = Database()
        self.db.start()

    def start( self):
        self.readConfiguration()
        self.showInfo()
        self.startDatabase()
        self.mainLoop()
        print( 'Servidor finalizado!!!')

    def readConfiguration( self):
        self._cfg = ServerConfig()

    def mainLoop(self):
        ThreadedServer( self.config.bindAddress, self.config.port, timeout=86400, callback=clientCallback, debug=True).start()
    #mainLoop

    def showInfo( self ):
        print( "VAGOAMIN: Vara de Goiabeira no Ambientalmente Incorreto.")
        print( 'Servido didático da disciplina de Protocolos de Aplicação.')
        print( 'Prof.: Leonidas Francisco de Lima Junior')
        print( "Aluno: Rogerlais Andrade e Silva")
        print( "Versão: %s" % CONSTANTS.APP_VERSION)
    #showInfo

def clientCallback(client, address, data):
    # send a response back to the client
    print('Dado recebido', data)
    try:
        #todo lembrar de incorporar IP do cliente nos dados
        hostRequest = DataWrapper.loadFromJSON( data )
        ret = json.loads(hostRequest.asJSON)
        ThreadLock.acquire()  #todo caso esta serialização comlique, montar dispatcher não bloqueante
        try:
            reponse = parada!
            ret = response.process()
        finally:
            ThreadLock.release()
        client.send(ret.encode('utf-8'))
    except Exception as e:
        print( e )
