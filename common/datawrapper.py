import json
from sys import prefix


class DataWrapper():

    def __init__(self, verb, data, retcode, msg):
        super().__init__()
        self._verb = verb
        self._json =  json.dumps( data )  #armazena string
        self._retcode = retcode
        self._msg = msg

    @property
    def verb(self):
        return self._verb

    @property
    def data( self ):
        return json.loads( self._json )

    @property
    def json(self):
        return self._json

    @property
    def retcode(self):
        return self._retcode

    @property
    def msg(self):
        return self._msg

    @staticmethod
    def loadFromJSON(jsonStr):
        ret = DataWrapper(None, None, None, None)
        ret._verb = jsonStr["verb"]
        ret._json = jsonStr["json"]
        ret._retcode = jsonStr["retcode"]
        ret._msg = jsonStr["msg"]
        return ret
