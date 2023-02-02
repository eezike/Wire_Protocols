import tkinter as tk
import backend.database as database
from frontend.loginpage import LoginPage

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.geometry("400x350")
        self.switch_frame(LoginPage)
        self.title("Chatroom")
        self.geometry("850x300")
        # Use one instance of a database per application--put in master variable
        self.db = database.Database()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()