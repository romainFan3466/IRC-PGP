
class Message:
    pass


    @staticmethod
    def rawParse(encodedMessage:str=""):
        pt = {}
        if "PRIVMSG" in encodedMessage:
            raw_user, type, target, raw_message = encodedMessage.split(sep=" ",maxsplit=3)
            user = raw_user[1:]
            user = user.split(sep="!")[0]
            message = raw_message[1:]
            pt["username"] = '<span style="color:blue; font-weight: bolder;">' + user + "</span>"
            pt["target"] = target
            pt["message"] = message
        return pt