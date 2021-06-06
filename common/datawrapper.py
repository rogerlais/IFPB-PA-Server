import json
from sys import prefix


class DataWrapper():

    def __init__(self, verb, json, retcode, msg):
        super().__init__()
        self._verb = verb
        self._json =  json  #armazena string
        self._retcode = retcode
        self._msg = msg

    @property
    def verb(self):
        return self._verb

    @property
    def data( self ):
        return json.loads( self._json )

    @property
    def retcode(self):
        return self._retcode

    @property
    def msg(self):
        return self._msg

    @staticmethod
    def loadFromJSON(jsonStr):
        ret = DataWrapper(None, None, None, None)
        ret._verb = jsonStr["_verb"]
        ret._json = jsonStr["_json"]
        ret._retcode = jsonStr["_retcode"]
        ret._msg = jsonStr["_msg"]
        return ret

    @property
    def asJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)