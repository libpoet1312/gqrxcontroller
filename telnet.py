import telnetlib
tn_ip = '127.0.0.1'
tn_port = 7356


class TelnetClient:
    client = None
    freq = None
    mod = None

    def __init__(self):
        pass

    def connect(self):
        try:
            tn = telnetlib.Telnet(tn_ip, tn_port)
        except Exception as e:
            print(e, flush=True)
            return
        else:
            self.client = tn

    def close(self):
        self.mod = None
        self.freq = None
        self.client.close()
        self.client = None

    def read_output(self):
        """
            Returns the read stream.
            Returns:
                result(str): The telnet response as a string
        """
        while 1:
            result = self.client.read_very_eager().decode('utf-8').split('\n')[0]
            if result:
                break
        return result

    async def get_freq(self):
        self.client.write(b"f\n")

        return self.read_output()

    async def get_mod(self) -> str:
        self.client.write(b"m\n")
        return self.read_output()

    async def send(self, command, value) -> str:
        string = command + ' ' + value + '\n'
        self.client.write(string.encode())
        return self.read_output()

    def set_debug_level(self, level):
        self.client.set_debuglevel(100)