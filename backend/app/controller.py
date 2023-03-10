import logging
from telnetlib import Telnet
from typing import Any

from pydantic import BaseModel, PrivateAttr

from config import Settings

logger = logging.getLogger(__name__)

settings = Settings()


class Controller(BaseModel):
    freq: str | None = None
    mod: str | None = None
    active: bool | None = None
    _client = PrivateAttr()
    debug_level: int = 0

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data: Any):
        super().__init__(**data)

    async def connect(self):
        if not self.active:
            try:
                tn = Telnet(settings.telnet_host, settings.telnet_port)
            except Exception as e:
                return None
            else:
                self._client = tn
                self.active = True
                return tn
        else:
            self.mod = None
            self.freq = None
            self._client.close()
            self._client = None

    def read_output(self):
        """
            Returns the read stream.
            Returns:
                result(str): The telnet response as a string
        """
        while 1:
            result = self._client.read_very_eager().decode('utf-8').split('\n')[0]
            if result:
                break
        return result

    def get_freq(self):
        self._client.write(b"f\n")

        return self.read_output()

    def get_mod(self) -> str:
        self._client.write(b"m\n")
        return self.read_output()

    async def send(self, command, value) -> str:
        string = command + ' ' + value + '\n'
        self._client.write(string.encode())
        return self.read_output()

    def set_debug_level(self, level):
        self._client.set_debuglevel(level)
