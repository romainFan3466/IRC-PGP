import requests
import json
from app import config
from app.core.ircPgpError import IrcPgpConnectionError

class APIhandler:

    session = {}
    api_host = config["HOST_API"]
    user = ""
    server_host =""
    states = {
        "api_logged" : False,
        "irc_logged" : False,
        "channel_joined" : False
    }


    def __init__(self):
        self.session = requests.Session()


    def login(self, user:str, password:str):
        credentials = {
            "login" : user,
            "password" : password
        }
        try:
            r = self.session.post(self.api_host+ "/users/login", data=credentials)
        except Exception:
            raise IrcPgpConnectionError("API", "login")
        else:
            status_code = r.status_code
            if status_code == 200:
                self.states["api_logged"]  = True
                self.user = user
            else:
                raise IrcPgpConnectionError("API", "login")


    def logout(self):
        if self.states["api_logged"]:
            for state in self.states:
                state = False
            r = self.session.get(self.api_host+"/users/logout")


    def connectIrcServer(self, username, host, port:int=6666):
        if not self.states["api_logged"]:
            raise IrcPgpConnectionError("API", "connect Irc Server")

        server = {
            "host": host,
            "port": port,
            "username": username
        }

        r = self.session.post(self.api_host+"/ircServers/connect",data=server)

        if r.status_code == 200:
            self.states["irc_logged"] =True
            self.server_host = host
            self.port = port
            self.username = username

        else:
            raise IrcPgpConnectionError("API", "connect Irc Server")


    def joinChannel(self, channel):
        if not self.states["api_logged"] or not self.states["irc_logged"]:
            raise IrcPgpConnectionError("API", "join")

        ch = str(channel).replace("#","",1)
        r = self.session.get(self.api_host+"/ircServers/join/" + ch)

        if r.status_code == 200:
            self.states["channel_joined"] = True
            self.channel = channel

        else:
            raise IrcPgpConnectionError("API", "join")


    def getAllPublicKeys(self):
        if not self.states["api_logged"] or not self.states["irc_logged"] or not self.states["channel_joined"]:
            raise IrcPgpConnectionError("API", "get All public Keys")
        r = self.session.get(self.api_host+"/publicKeys/getAll")
        if r.status_code == 200:
            return r.json()["publicKeys"]
        else:
            raise IrcPgpConnectionError("API", "get All public Keys")


    def updatePublicKey(self, public_key:str=""):
        if not self.states["api_logged"] or not self.states["irc_logged"] or not self.states["channel_joined"]:
            raise IrcPgpConnectionError("API", "update public key")

        pk = {"public_key" : public_key}
        r = self.session.post(self.api_host+"/publicKeys/update",data=pk)
        if r.status_code != 200:
            raise IrcPgpConnectionError("API", "update public key")