import tkinter as tk
from tkinter import messagebox
from frontend.homepage import HomePage
from frontend.registerpage import RegisterPage

class LoginPage(tk.Frame):
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
        
        # Create label for username
        self.username_label = tk.Label(self, text="Username:", font=("TkDefaultFont", 16))
        self.username_label.grid(row=2, column=0, padx=10, pady=10)
        
        # Create entry for username
        self.username_entry = tk.Entry(self, font=("TkDefaultFont", 14))
        self.username_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Create label for password
        self.password_label = tk.Label(self, text="Password:", font=("TkDefaultFont", 16))
        self.password_label.grid(row=3, column=0, padx=10, pady=10)
        
        # Create entry for password
        self.password_entry = tk.Entry(self, font=("TkDefaultFont", 14), show="*")
        self.password_entry.grid(row=3, column=1, padx=10, pady=10)
        
        # Create login button
        self.login_button = tk.Button(self, text="Login", font=("TkDefaultFont", 14), command=self.login)
        self.login_button.grid(row=4, column=0, pady=10, padx=10, sticky="W")

        # Create register button
        self.register_button = tk.Button(self, text="Register", font=("TkDefaultFont", 14), command=self.register)
        self.register_button.grid(row=4, column=1, pady=10, padx=10, sticky="E")

    def connect(self):
        host = self.host_entry.get()
        port = self.port_entry.get()
        

    
    def login(self):
        self.connect()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.master.db.login(username, password) == None:
            messagebox.showerror("Login Failed", "Invalid username or password")
        else:
            messagebox.showinfo("Login Successful", "Welcome " + username + "!")
            self.master.switch_frame(HomePage)

    def register(self):
        self.master.switch_frame(RegisterPage)