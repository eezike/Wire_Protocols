import tkinter as tk
from frontend.connectpage import ConnectPage
from frontend.loginpage import LoginPage
from frontend.homepage import HomePage
from backend.client import Client 

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # Initialize instance variables
        self._frame = None
        self.client : Client = Client()

        # Set title and window size
        self.title("Chatroom")
        self.geometry("850x300")
        
        # Switch to the ConnectPage
        self.switch_frame(0)

    # Function to switch to a new frame
    def switch_frame(self, frame_class_index : int):

        # choose frame class by index
        frame_class = [ConnectPage, LoginPage, HomePage][frame_class_index]

        # Create a new frame instance
        new_frame = frame_class(self)
        
        # Destroy the old frame if it exists
        if self._frame is not None:
            self._frame.destroy()

        # Set the new frame as the current frame and pack it
        self._frame = new_frame
        self._frame.pack()

def run():
    # Create an instance of Application and start the mainloop
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    run()