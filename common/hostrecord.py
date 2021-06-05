

class HostRecord():

    def __init__(self) -> None:
        super.__init__(self)
        self._hostname = None
        self._MAC = None
        self._loggedUser = None
        self._timestamp = None
        #todo ver demais atributos
    #construtor

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

