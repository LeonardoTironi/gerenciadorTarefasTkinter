from model import Model
import bcrypt
class Controller:
    def __init__(self):
        self.model = Model()
    
    def setUser(self, user, password:str):
        salt = bcrypt.gensalt()
        return self.model.setUser(user, bcrypt.hashpw(password.encode('utf-8'), salt))
    def auth(self, user, password):
        return self.model.auth(user, password)