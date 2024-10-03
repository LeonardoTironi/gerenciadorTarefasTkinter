from model import Model
class Controller:
    def __init__(self):
        self.model = Model()
    
    def setUser(self, user, password:str, password2:str):
        return self.model.setUser(user, password, password2)
    def auth(self, user, password):
        return self.model.auth(user, password)
    def setView(self, view):
        self.view = view

    