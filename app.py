import tkinter as tk
import backend.database as database
from frontend.loginpage import LoginPage
from backend.client import Client 

class Application(tk.Tk):
    def __init__(self, client):
        tk.Tk.__init__(self)
        self._frame = None
        self.geometry("400x350")
        self.switch_frame(LoginPage)
        self.title("Chatroom")
        self.geometry("850x300")
        # Use one instance of a database per application--put in master variable
        self.db = database.Database()
        self.client = client

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

def run(client):
    app = Application(client)
    app.mainloop()

run(Client())