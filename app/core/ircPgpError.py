
class IrcPgpConnectionError(Exception):

    def __init__(self, module, action):
        self.module= module
        self.action = action


    def __str__(self):
        return "Module : "+ str(self.module) +" - Action : "+ str(self.action) + " failed"


