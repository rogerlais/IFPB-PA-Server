import json
from sys import prefix
from common.hostrecord import HostRecord


# Deserializa como HostRecord
def decodeHostRecord(dct):
    #!if "__complex__" in dct: poderia haver teste de assinatura de classe
    if "_hostname" in dct:
        ret = HostRecord(dct["_hostname"], dct["_MAC"],  dct["_address"], dct["_loggedUser"])
    elif("hostname" in dct):
        ret = HostRecord(dct["hostname"], dct["MAC"],  dct["address"], dct["loggedUser"])
    else:
        ret = dct  # todo retorna o que se não tem a assinatura??? return dct ??
    return ret


def decodeDataWrapper(dct):
    if "_verb" in dct:
        ret = DataWrapper(dct["_verb"], dct["_hostAsJSON"],  dct["_retcode"], dct["_msg"])
    elif("verb" in dct):
        ret = DataWrapper(dct["verb"], dct["hostAsJSON"],  dct["retcode"], dct["msg"])
    else:
        ret = dct  # todo retorna o que se não tem a assinatura??? return dct ??
    return ret


class DataWrapper():

    def __init__(self, verb, hostAsJSON, retcode, msg):
        super().__init__()
        self._verb = verb
        self._hostAsJSON = hostAsJSON  # armazena string
        self._retcode = retcode
        self._msg = msg

    @staticmethod
    def loadFromJSON(jsonStr):
        ret = json.loads(jsonStr, object_hook=decodeDataWrapper)
        return ret

    @property
    def verb(self):
        return self._verb

    @property
    def host(self):
        # todo testar alteração para retornar HostRecord no lugar de  Dict
        return json.loads(self._hostAsJSON, object_hook=decodeHostRecord)

    @property
    def retcode(self):
        return self._retcode

    @property
    def msg(self):
        return self._msg

    @property
    def hostAsJSON(self):
        return self._hostAsJSON

    @property
    def asJSON(self):
        ret = json.dumps(self, default=lambda o: o.__dict__)
        return ret
