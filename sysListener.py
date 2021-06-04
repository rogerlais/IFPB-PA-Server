#TODO: generate class doc

class SysEvent():

    def __init__(self) -> None:
        super.__init__(self)
        self._isSystemDown = False

    @property
    def isSystemDown(self):
        self.updateSystemStatus()
        return self._isSystemDown

    def updateSystemStatus( self ):
        self._isSystemDown = False