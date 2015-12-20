import irc.client
from app.models.message import Message
import threading

class IRChandler:

    host = ""
    port = ""
    password = ""
    channel = ""
    client = None
    reactor = None
    process_forever = None
    __signal = False


    def __init__(self, host:str, username:str, port:int=6666, password:str=None):
        self.host = host
        self.port = port
        self.password = password
        self.username = username
        self.__init_server()


    def __init_server(self):
        self.reactor = irc.client.Reactor()
        self.client = self.reactor.server()


    def connect(self):
        try:
            self.client.connect(self.host, self.port, self.username,password=self.password)
        except irc.client.ServerConnectionError:
            return False
        self.client.set_keepalive(60)
        self.process_forever = threading.Thread(target=self.__process)
        self.__signal = True
        # self.process_forever.start()
        return True


    def join(self, channel:str):
        self.channel = channel
        self.client.join(channel)
        return True

    def __process(self):
        while self.__signal:
            self.reactor.process_once(timeout=0.2)

    def sendMessage(self, message):
        self.client.privmsg(self.channel, message)


    def getBuffer(self):
        return self.client.socket.recv(1024).decode("utf-8")

    def is_connected(self):
        return self.client.is_connected()

    def stop(self):
        if self.client.is_connected():
            self.client.quit()
        if self.process_forever is not None and self.process_forever.is_alive() :
            self.__signal = False