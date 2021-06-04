#! refs https://www.sqlitetutorial.net/sqlite-python/

# TODO: Doc to file/class

import sqlite3
from sqlite3 import Error
import os


class Database():

    def __init__(self):
        super().__init__()
        self._conn = None
        self._dbFile = os.path.join(os.path.abspath('./dbfiles'), 'vagoamin.db')

    @property
    def conn(self):
        return self._conn

    @property
    def dbFile(self):
        return self._dbFile

    def createTable(self, sql):
        try:
            c = self._conn.cursor()
            c.execute(sql)
        except Error as e:
            (e)

    def createHostTable(self):
        sql = """
        CREATE TABLE hosts (
                id        INTEGER     PRIMARY KEY AUTOINCREMENT,
                name      TEXT (25)   CONSTRAINT [uniq-name] UNIQUE,
                IPV4      TEXT (16),
                online    BOOLEAN     DEFAULT (false),
                lastcheck DATETIME,
                MAC       STRING (20)
            );
        """
        self.createTable(sql)

    def forceDir(self, fname):
        p = os.path.dirname(fname)
        try:
            if( not os.path.exists( p )):
                os.makedirs(p)
        except:
            raise 'Base de dados não pode ser criada em {0}'.format(self.dbFile)

    def createDB(self):
        print('Criando base de dados em {0}'.format(self.dbFile))
        self.forceDir(self.dbFile)

    def start(self):
        tablesPending = False
        if(not os.path.exists(self.dbFile)):
            self.createDB()
            tablesPending = True
        try:
            self._conn = sqlite3.connect(self.dbFile)
            print('Base de dados conectada. Engine({0})'.format( sqlite3.version ))
        except Error as e:
            print(e)
        self.migrate( tablesPending )


    def migrate( self, recreate ):
        if( recreate ):
            self.createHostTable()
        else:
            #todo verificar tabela de versão, etc....
            return
        return

    def stop(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def writeHostRecord(self, hostRec):
        print("Não implementada ")
        return None

    def readHostStatus(self, hostRec):
        print("Não implementado")
