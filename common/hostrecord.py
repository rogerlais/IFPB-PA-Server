import json
import datetime;
import common.constants as CONSTANTS

class HostRecord():

    def __init__(self, hostname, MAC, address, loggedUser ):
        super().__init__()
        self._hostname = hostname
        self._MAC = MAC
        self._address = address
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
    def address( self ):
        return self._address

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

    @property
    def asJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def dummyAsJSON( self ):
        ret = json.dumps( self )
        #meDict = [ { 'hostname': self.hostname, 'MAC': self._MAC, 'loggedUser': self.loggedUser, "timestamp": self.timestamp }]
        #ret = json.dumps(meDict)
        return ret