import irc.client
from app.models.message import Message

class IRChandler:

    host = ""
    port = ""
    password = ""
    channel = ""
    client = None
    reactor = None


    def __init__(self, host:str, username:str, port:int=6666, password:str=""):
        self.host = host
        self.port = port
        self.password = password
        self.username = username

        self.__init_server()

    def __init_server(self):
        self.reactor = irc.client.Reactor()
        self.client = self.reactor.server()

    def connect(self):
        self.client.connect(self.host, self.port, self.username,self.password)
        return self.client.is_connected()

    def join(self, channel:str):
        self.client.join(channel)
        return


    def sendMessage(self, message:Message):
        pass


