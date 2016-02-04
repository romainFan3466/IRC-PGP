
class Observer(object):

        def update(self, buffer):
            pass

        def updateNames(self, buffer):
            pass

class Observable(object):

    observer = None

    def addObserver(self, obs):
        self.observer = obs

    def notifyObserver(self, buffer="", method=""):
        if self.observer is not None:
            if method == "namelist":
                self.observer.updateNames(buffer=buffer)
            else:
                self.observer.update(buffer=buffer)