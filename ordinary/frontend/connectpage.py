import tkinter as tk
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
        self.host_entry.insert(0, '10.250.74.51')

        # Create label for port
        self.port_label = tk.Label(self, text="Port:", font=("TkDefaultFont", 16))
        self.port_label.grid(row=1, column=0, padx=10, pady=10)
        
        # Create entry for port
        self.port_entry = tk.Entry(self, font=("TkDefaultFont", 14))
        self.port_entry.grid(row=1, column=1, padx=10, pady=10)
        self.port_entry.insert(0, '9999')
        
        # Create connect button
        self.connect_button = tk.Button(self, text="Connect", font=("TkDefaultFont", 14), command=self.connect)
        self.connect_button.grid(row=2, column=0, pady=10, padx=10, sticky="W")


    # a method to establish a connection with the given host and port
    def connect(self):
        # extract the host and port values from the respective entries
        host = self.host_entry.get()
        port = self.port_entry.get()

        # validate if port is an integer
        try:
            port = int(port)
        except:
            # if not, show an error message box and return from the method
            messagebox.showerror("Input Error", "Port must be an integer")
            return

        # attempt to connect to the server with the given host and port
        if self.master.client.connect(host, port):
            # if the connection is successful, switch the frame to the login page
            self.master.switch_frame(1)
        else:
            # if the connection is not successful, show an error message box with an appropriate message
            messagebox.showerror("Connection Timeout", "Invalid host or port")
