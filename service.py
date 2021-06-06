from database import Database
from serverconfig import ServerConfig
import common.constants as CONSTANTS
from common.datawrapper import DataWrapper, decodeDataWrapper
from server import ThreadedServer
from threading import RLock


import json
import time

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
        ThreadedServer( self, self.config.bindAddress, self.config.port, timeout=86400, callback=clientCallback, debug=True).start()
    #mainLoop

    def getResponse( self, req ):
        host = req.host
        if( req.verb == CONSTANTS.VERB_GET_VERSION ):
            res = DataWrapper( req.verb, req.asJSON , 0 , CONSTANTS.APP_VERSION )
        elif( req.verb == CONSTANTS.VERB_BYE ):
            res = DataWrapper( req.verb, req.asJSON , 0 , CONSTANTS.VERB_BYE )
        elif( req.verb == CONSTANTS.VERB_UPDATE ):
            #todo testar a situação do host e enviar o comando de desligamento ao invés de poweron
            res = DataWrapper( req.verb, req.asJSON , 0 , CONSTANTS.VERB_POWEROFF )
        else:
            res = DataWrapper( req.verb, req.asJSON , CONSTANTS.RESP_ERROR , 'Comando não reconhecido pelo protolo' )
        return res

    def showInfo( self ):
        print( "VAGOAMIN: Vara de Goiabeira no Ambientalmente Incorreto.")
        print( 'Servido didático da disciplina de Protocolos de Aplicação.')
        print( 'Prof.: Leonidas Francisco de Lima Junior')
        print( "Aluno: Rogerlais Andrade e Silva")
        print( "Versão: %s" % CONSTANTS.APP_VERSION)
    #showInfo

def clientCallback(serviceThread, sockClient, address, jsonDict):
    # send a response back to the client
    print('Dado recebido', jsonDict)
    try:
        #todo lembrar de incorporar IP do cliente nos dados
        dw = decodeDataWrapper( jsonDict )
        ThreadLock.acquire()  #todo caso esta serialização comlique, montar dispatcher não bloqueante
        try:
            dwRes = serviceThread.server.getResponse( dw )
            res = dwRes.asJSON
            #ret = response.process()
        finally:
            ThreadLock.release()
        sockClient.send(res.encode('utf-8'))
        if( dwRes.verb == CONSTANTS.VERB_BYE ):
            time.sleep( 2 )
            sockClient.close()
    except Exception as e:
        #todo tratar erro e responder ao cliente o ocorrido
        print( e )
