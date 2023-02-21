import sqlite3
from contextlib import closing

import sqlite3
from contextlib import closing

class Database:
    def __init__(self, name="chatroom.db"):
        # If no database name is provided, use the default name
        if name == None:
            name = "chatroom.db"

        # Connect to the database
        self.conn = sqlite3.connect(name, check_same_thread=False)

        # Create Users and Messages tables if they don't exist
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS Users (username TEXT PRIMARY KEY, password TEXT NOT NULL)""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS Messages (id INTEGER PRIMARY KEY, recipient TEXT, sender TEXT, message TEXT NOT NULL, FOREIGN KEY (recipient) REFERENCES Users(username), FOREIGN KEY (sender) REFERENCES Users(username)) """)
            self.conn.commit()
    
    def register(self, username: str, password: str) -> None:
        with closing(self.conn.cursor()) as cursor:
            # Check if the username already exists
            res = cursor.execute("SELECT username, password FROM Users WHERE username = ?", (username,)).fetchall()
            
            if len(res) > 0:
                raise Exception("Username already exists")

            # Insert new user into the database
            cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()

    def login(self, username: str, attempted_password: str) -> None:
        with closing(self.conn.cursor()) as cursor:
            # Check if the username exists
            res = cursor.execute("SELECT username, password FROM Users WHERE username = ?", (username,)).fetchall()

            if len(res) != 1:
                raise Exception("Account does not exist")
            
            _, password = res[0]
            
            # Check if the password matches
            if password != attempted_password:
                raise Exception("Incorrect password")
            
    def save_message(self, sender: str, recipient: str, content: str) -> None:
        with closing(self.conn.cursor()) as cursor:
            # Insert a message into the Messages table
            cursor.execute("INSERT INTO Messages (recipient, sender, message) VALUES (?, ?, ?)", (recipient, sender, content))
            self.conn.commit()

    def delete_message(self, msg_id: int) -> None:
        with closing(self.conn.cursor()) as cursor:
            # Delete a message from the Messages table based on its id
            cursor.execute("DELETE FROM Messages WHERE id = ?", (msg_id,))
            self.conn.commit()

    def get_messages(self, username: str):
        with closing(self.conn.cursor()) as cursor:
            # Get messages from the Messages table based on the recipient's username
            res = cursor.execute("SELECT id, sender, message FROM Messages WHERE recipient = ?", (username,)).fetchall()
            
            for msg_id, _, _ in res:
                # Delete messages that have been retrieved
                self.delete_message(msg_id)
            
            # Return a list of tuples of the sender and the content of the messages retrieved
            return [(sender, content) for _, sender, content in res]
    
    def get_users(self) -> list[str]:
        with closing(self.conn.cursor()) as cursor:
            # Get a list of all usernames from the Users table
            res = cursor.execute("SELECT username FROM Users").fetchall()

            return [name for (name,) in res]

    def delete_user(self, username: str):
        with closing(self.conn.cursor()) as cursor:
            # Check if the user exists in the Users table
            res = cursor.execute("SELECT username FROM Users WHERE username = ?", (username,)).fetchall()
            if len(res) == 0:
                raise Exception("Account does not exist")

            # Delete the user from the Users table
            cursor.execute("DELETE FROM Users WHERE username = ?", (username,))
            self.conn.commit()

            # TODO: need to delete messages addressed to that user as well upon deletion



