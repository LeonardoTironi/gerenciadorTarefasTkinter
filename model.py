import sqlite3
import bcrypt
class Model:
    def __init__(self):
        self.con = sqlite3.connect('database.db', check_same_thread=False)
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users(id_peca INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT NOT NULL, password TEXT NOT NULL)")

    def setUser(self, user, password, password2):
        if self.camposRegistro(user, password, password2):
            return 1, "Escreva em todos os campos"
        if self.igualdade(password, password2):
            return 2, "As senhas são diferentes"
        if self.existencia(user):
            return 3, "Usuário já existe"
        salt = bcrypt.gensalt()
        password=bcrypt.hashpw(password.encode('utf-8'), salt)
        self.cursor.execute("INSERT INTO users(user, password) values(?, ?)", (user, password,))
        self.con.commit()
        return 0,""

    def auth(self, user, password):
        if self.camposLogin(user, password):
            return 1, "Escreva em todos os campos"
        if not self.existencia(user):
            return 4, "Usuário não existe"
        
        self.cursor.execute("Select password from users where user=?",(user, ))
        passC = self.cursor.fetchall()
        teste = bcrypt.checkpw(password.encode('utf-8'), passC[0][0])
        if teste:
            return 0, f"Bem vindo {user}"
        else:
            return 5, "Senha ou usuário incorreto"
    
    def existencia(self, user):
        self.cursor.execute("Select user from users where user=?",(user, ))
        res = self.cursor.fetchall()
        if res:
            return 1
        else:
            return 0
        
    def camposLogin(self, user, password):
        if user and password:
            return 0
        else:
            return 1
        
    def camposRegistro(self, user, password, password2):
        if user and password and password2:
            return 0
        else:
            return 1

    def igualdade(self, password, password2):
        if password==password2:
            return 0
        else:
            return 1
