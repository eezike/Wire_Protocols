import tkinter as tk
from frontend.loginpage import LoginPage
from tkinter import messagebox

class ConnectPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        # Create label for host
        self.host_label = tk.Label(self, text="Host:", font=("TkDefaultFont", 16))
        self.host_label.grid(row=0, column=0, padx=10, pady=10)
        
        # Create entry for host
        self.host_entry = tk.Entry(self, font=("TkDefaultFont", 14))
        self.host_entry.grid(row=0, column=1, padx=10, pady=10)
        self.host_entry.focus_set()

        # Create label for port
        self.port_label = tk.Label(self, text="Port:", font=("TkDefaultFont", 16))
        self.port_label.grid(row=1, column=0, padx=10, pady=10)
        
        # Create entry for port
        self.port_entry = tk.Entry(self, font=("TkDefaultFont", 14))
        self.port_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Create connect button and link to connect()
        self.connect_button = tk.Button(self, text="Connect", font=("TkDefaultFont", 14), command=self.connect)
        self.connect_button.grid(row=2, column=0, pady=10, padx=10, sticky="W")

    def connect(self):
        """
        Retreives host and port from frame and tries to connect server to server.
        """
        host = self.host_entry.get()
        port = self.port_entry.get()

        try:
            port = int(port)
        except:
            messagebox.showerror("Input Error", "Port must be an integer")
            return

        # Switch to login frame upon successful connect
        if self.master.client.connect(host, port):
            self.master.switch_frame(LoginPage)
        else:
            messagebox.showerror("Connection Timeout", "Invalid host or port")