
class Observer(object):

    def update(self, buffer=""):
        pass

class Observable(object):

    observer = None

    def addObserver(self, obs):
        self.observer = obs

    def notifyObserver(self, buffer=""):
        if self.observer is not None:
            self.observer.update(buffer=buffer)