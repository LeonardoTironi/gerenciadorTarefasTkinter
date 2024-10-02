import sqlite3
import bcrypt
class Model:
    def __init__(self):
        self.con = sqlite3.connect('database.db', check_same_thread=False)
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users(id_peca INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT NOT NULL, password TEXT NOT NULL)")

    def setUser(self, user, password):
        self.cursor.execute("Select password from users where user=?",(user, ))
        res = self.cursor.fetchall()
        if res:
            return 0
        else:
            self.cursor.execute("INSERT INTO users(user, password) values(?, ?)", (user, password,))
            self.con.commit()
            return 1

    def auth(self, user, password):
        self.cursor.execute("Select password from users where user=?",(user, ))
        passC = self.cursor.fetchall()
        print(passC[0])
        return bcrypt.checkpw(password.encode('utf-8'), passC[0][0])

