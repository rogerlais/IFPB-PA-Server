
class ServerConfig():
    def __init__(self) -> None:
        super().__init__()
        self._port = 8421
        self._fakeDelay = 0
        self._bindAddress = '0.0.0.0'

    @property
    def port(self):
        return self._port

    @property
    def fakeDelay(self):
        return self._fakeDelay

    @property
    def bindAddress(self):
        return self._bindAddress