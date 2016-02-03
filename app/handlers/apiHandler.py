import requests
import json
from app import config

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
        r = self.session.post(self.api_host+ "/users/login", data=credentials)
        status_code = r.status_code
        if status_code == 200:
            self.states["api_logged"]  = True
            self.user = user

        return status_code == 200


    def logout(self):
        if self.states["api_logged"]:
            for state in self.states:
                state = False
            r = self.session.get(self.api_host+"/users/logout")


    def connectIrcServer(self, username, host, port:int=6666):
        if not self.states["api_logged"]:
            return False

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

        return r.status_code == 200


    def joinChannel(self, channel):
        if not self.states["api_logged"] or not self.states["irc_logged"]:
            return False

        ch = str(channel).replace("#","",1)
        r = self.session.get(self.api_host+"/ircServers/join/" + ch)

        if r.status_code == 200:
            self.states["channel_joined"] = True
            self.channel = channel

        return r.status_code == 200


    def getAllPublicKeys(self):
        if not self.states["api_logged"] or not self.states["irc_logged"] or not self.states["channel_joined"]:
            return False
        r = self.session.get(self.api_host+"/publicKeys/getAll")
        public_keys = r.json() if r.status_code == 200 else None
        return public_keys


    def updatePublicKey(self, public_key:str=""):
        if not self.states["api_logged"] or not self.states["irc_logged"] or not self.states["channel_joined"]:
            return False

        pk = {"public_key" : public_key}
        r = self.session.post(self.api_host+"/publicKeys/update",data=pk)
        return r.status_code == 200