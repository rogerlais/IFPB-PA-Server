from database import Database
import os
import time
from serverconfig import ServerConfig
from workthread import WorkThread

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


    def showInfo():
        print( "Não implementado!!!")

    def start( self):
        self.readConfiguration()
        self.showInfo()
        self.startDatabase()
        self.mainLoop()
        print( 'Não implementado!!!')

    def readConfiguration( self):
        self._cfg = ServerConfig()

    def mainLoop(self):
        while True:
            #TODO: Create sockect and start listen to him
            wt = WorkThread( self.config.port, self.config.bindAddress )
            wt.run()
            if( self._sysListener.isSystemDown ):
                break
    #mainLoop

    def showInfo( self ):
        print( "VAGOAMIN: Vara de Goiabeira no Ambientalmente Incorreto.")
        print( 'Servido didático da disciplina de Protocolos de Aplicação.')
        print( 'Prof.: Leonidas Francisco de Lima Junior')
        print( "Aluno: Rogerlais Andrade e Silva")
        print( "" )
    #showInfo