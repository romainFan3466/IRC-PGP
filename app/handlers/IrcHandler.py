import irc.client
from app.models.message import Message
import threading
import logging
from app.core.Observer import Observable
from app.core.ircPgpError import IrcPgpConnectionError
import time
logging.basicConfig(level="DEBUG")

class IRChandler(Observable):

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
        self.client.add_global_handler('all_raw_messages', self.on_msg)


    def __init_server(self):
        self.reactor = irc.client.Reactor()
        self.client = self.reactor.server()


    def connect(self):
        try:
            self.client.connect(self.host, self.port, self.username,password=self.password)
        except irc.client.ServerConnectionError:
            raise IrcPgpConnectionError("IRC", "connection")
        else:
            self.client.set_keepalive(20)
            self.process_forever = threading.Thread(target=self.__process)
            self.__signal = True
            self.process_forever.start()


    def join(self, channel:str):
        self.channel = channel
        self.client.join(channel)


    def __process(self):
        while self.__signal:
            self.reactor.process_once(timeout=0.2)

    def getUserName(self):
        return self.username


    def sendMessage(self, message):
        self.client.privmsg(self.channel, message)


    def on_msg(self, connection, event):
        if not "PONG" in event.arguments[0]:
            self.notifyObserver(event.arguments[0])


    def is_connected(self):
        return self.client.is_connected()

    def stop(self):
        self.client.remove_global_handler("all_raw_messages", self.on_msg)
        if self.client.is_connected():
            self.client.quit()
        if self.process_forever is not None and self.process_forever.is_alive() :
            self.__signal = False