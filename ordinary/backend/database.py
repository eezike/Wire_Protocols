import sqlite3
from contextlib import closing

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("chatroom.db", check_same_thread=False)

        # Creates Users and Messages table if it does not exist
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS Users (username TEXT PRIMARY KEY, password TEXT NOT NULL)""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS Messages (id INTEGER PRIMARY KEY, recipient TEXT, sender TEXT, message TEXT NOT NULL, FOREIGN KEY (recipient) REFERENCES Users(username), FOREIGN KEY (sender) REFERENCES Users(username)) """)
            
            self.conn.commit()
    
    def register(self, username:str, password:str) -> None:
        with closing(self.conn.cursor()) as cursor:
            res = cursor.execute("SELECT username, password FROM Users WHERE username = ?", (username,)).fetchall()
            
            if len(res) > 0:
                raise Exception("Username already exists")

            cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
            
            self.conn.commit()

    def login(self, username: str, attempted_password: str) -> None:
        with closing(self.conn.cursor()) as cursor:
            res = cursor.execute("SELECT username, password FROM Users WHERE username = ?", (username,)).fetchall()

            if len(res) != 1:
                raise Exception("Account does not exist")
            
            _, password = res[0]
            
            if password != attempted_password:
                raise Exception("Incorrect password")
            
        

    def save_message(self, sender: str, recipient: str, content: str) -> None:
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("INSERT INTO Messages (recipient, sender, message) VALUES (?, ?, ?)", (recipient, sender, content))
            self.conn.commit()

    def delete_message(self, msg_id: int) -> None:
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("DELETE FROM Messages WHERE id = ?", (msg_id,))
            self.conn.commit()

    def get_messages(self, username: str):
        with closing(self.conn.cursor()) as cursor:
            res = cursor.execute("SELECT id, sender, message FROM Messages WHERE recipient = ?", (username,)).fetchall()
            
            for msg_id, _, _ in res:
                self.delete_message(msg_id)
            
            return [(sender, content) for _, sender, content in res]
    
    def get_users(self) -> list[str]:
        with closing(self.conn.cursor()) as cursor:
            res = cursor.execute("SELECT username FROM USERS").fetchall()

            return [name for (name,) in res]

    def delete_user(self, username: str):
        with closing(self.conn.cursor()) as cursor:

            res = cursor.execute("SELECT username FROM Users WHERE username = ?", (username,)).fetchall()
            if len(res) == 0:
                raise Exception("Account does not exist")

            cursor.execute("DELETE FROM Users WHERE username = ?", (username,))
            self.conn.commit()

            # TODO: need to delete messages addressed to that user as well upon deletion
