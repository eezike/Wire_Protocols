import tkinter as tk
from frontend.connectpage import ConnectPage
from backend.client import Client 

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(ConnectPage)
        self.title("Chatroom")
        self.geometry("850x300")
        self.client : Client = Client()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

def run():
    app = Application()
    app.mainloop()

run()