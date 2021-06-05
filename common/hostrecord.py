import json
import datetime;
import common.constants as CONSTANTS

class HostRecord():

    def __init__(self, hostname, MAC, Address, loggedUser ):
        super().__init__()
        self._hostname = hostname
        self._MAC = MAC
        self._loggedUser = loggedUser
        self._timestamp =  datetime.datetime.now().timestamp()
        #todo ver demais atributos
    #construtor


    @staticmethod
    def loadFromJSON( jsonStr ):
        ret = HostRecord( None, None, None, None)
        s = jsonStr[len( CONSTANTS.DATAHEADER ):]
        dic = json.loads( s )
        ret._hostname = dic["hostname"]
        ret._MAC = dic["MAC"]
        ret._loggedUser = dic["loggedUser"]
        ret._timestamp =  dic["timestamp"]
        return ret


    @staticmethod
    def getFromComputer():
        ret = HostRecord( 'fake-pcname', 'fak-mac', 'fake-addr', 'fake-user')
        return ret

    @property
    def hostname( self ):
        return self._hostname

    @property
    def MAC( self ):
        return self._MAC

    @property
    def loggedUser( self ):
        return self._loggedUser

    @property
    def timestamp( self ):
        return self._timestamp

    def export( self ):
        meDict = {'hostname': self.hostname, 'MAC': self._MAC, 'loggedUser': self.loggedUser, "timestamp": self.timestamp }
        ret = json.dumps(meDict)
        return ret