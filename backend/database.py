import sqlite3
from contextlib import closing

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("chatroom.db")

        # Creates Users and Messages table if it does not exist
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS Users (username TEXT PRIMARY KEY, password TEXT NOT NULL)""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS Messages (id INTEGER PRIMARY KEY, _to TEXT, _from TEXT, message TEXT NOT NULL, FOREIGN KEY (_to) REFERENCES Users(username), FOREIGN KEY (_from) REFERENCES Users(username)) """)
            
            self.conn.commit()
    
    def register(self, username:str, password:str) -> str:
        with closing(self.conn.cursor()) as cursor:
            res = cursor.execute("SELECT username, password FROM Users WHERE username = ?", (username,)).fetchall()
            if len(res) > 0:
                print("Error: [register] account exists")
                return

            cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
            
            self.conn.commit()
        
        return username

    def login(self, username: str, attempted_password: str) -> str:
        with closing(self.conn.cursor()) as cursor:
            res = cursor.execute("SELECT username, password FROM Users WHERE username = ?", (username,)).fetchall()

            if len(res) != 1:
                print("Error: [login] Account does not exist")
                return
            
            _, password = res[0]
            
            if password != attempted_password:
                print("Error: [login] Wrong password")
                return
            
        return username

        def logout():
            return

    def save_message(self, _to: str, _from: str, msg: str) -> None:
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("INSERT INTO Messages (_to, _from, message) VALUES (?, ?, ?)", (_to, _from, msg))
            self.conn.commit()

    def delete_message(self, msg_id: int) -> None:
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("DELETE FROM Messages WHERE id = ?", (msg_id,))
            self.conn.commit()

    def get_messages(self, username: str):
        with closing(self.conn.cursor()) as cursor:
            res = cursor.execute("SELECT id, _from, message FROM Messages WHERE _to = ?", (username,)).fetchall()
            
            for msg_id, _, _ in res:
                self.delete_message(msg_id)
            
            return [(_from, msg) for _, _from, msg in res]

    def delete_user(self, username: str):
        with closing(self.conn.cursor()) as cursor:

            res = cursor.execute("SELECT username FROM Users WHERE username = ?", (username,)).fetchall()
            if len(res) == 0:
                print("Error: [delete_user] account does not exist")
                return

            cursor.execute("DELETE FROM Users WHERE username = ?", (username,))
            self.conn.commit()

            # TODO: need to delete messages addressed to that user as well upon deletion
