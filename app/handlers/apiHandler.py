import requests
import json
from app import config

class APIhandler:

    session = {}
    host = config["HOST_API"]

    def __init__(self):
        self.session = requests.Session()

    def login(self, user:str, password:str):
        credentials = {
            "user" : user,
            "password" : password
        }

        r = self.session.post(host + /", data=json.dumps(data),  verify=False)
















s = requests.Session()


r = s.get("https://deliverytracker.romainfanara.com/api/status", verify=False)

print(r.json())

data = {
    "user":{
        "email" : "romain.fanara@gmail.com",
        "password" : "1234"
    }
}


r = s.post("https://deliverytracker.romainfanara.com/api/signIn", data=json.dumps(data),  verify=False)
print(r.json())


r = s.get("https://deliverytracker.romainfanara.com/api/status",  verify=False)

print(r.json())