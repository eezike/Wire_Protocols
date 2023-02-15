import tkinter as tk
from tkinter import messagebox
from frontend.homepage import HomePage
import backend.wireprotocol as wp

class LoginPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        if self.master.client.connected == False:
            messagebox.showerror("Error", "Not connected")
            return
  
        # Create label for username
        self.username_label = tk.Label(self, text="Username:", font=("TkDefaultFont", 16))
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        
        # Create entry for username
        self.username_entry = tk.Entry(self, font=("TkDefaultFont", 14))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.username_entry.focus_set()
        
        # Create label for password
        self.password_label = tk.Label(self, text="Password:", font=("TkDefaultFont", 16))
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        
        # Create entry for password
        self.password_entry = tk.Entry(self, font=("TkDefaultFont", 14), show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Create login button
        self.login_button = tk.Button(self, text="Login", font=("TkDefaultFont", 14), command=self.login)
        self.login_button.grid(row=2, column=0, pady=10, padx=10, sticky="W")

        # Create register button
        self.register_button = tk.Button(self, text="Register", font=("TkDefaultFont", 14), command=self.register)
        self.register_button.grid(row=2, column=1, pady=10, padx=10, sticky="E")

        
    def login(self):
        if self.master.client.connected == False:
            messagebox.showerror("Error", "Not connected")
            return

        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check server response before logging in
        if len(username) == 0 or len(password) == 0:
            messagebox.showerror("Login Failed", "Username or password cannot be empty")
            return
        
        if len(username) > 20 or len(password) > 20:
            messagebox.showerror("Login Failed", "Invalid username or password")
            return

        response = self.master.client.send_login(username, password)

        if response == wp.RESPONSE_CODE.LOGIN_SUCCESS:
            messagebox.showinfo("Login Successful", "Welcome " + username + "!")
            self.master.switch_frame(HomePage)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            
    def register(self):

        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if input is valid
        if len(username) == 0 or len(password) == 0:
            messagebox.showerror("Register Failed", "Username or password cannot be empty")
            return
        elif len(username) > 20 or len(password) > 20:
            messagebox.showerror("Register Failed", "Username or password cannot exceed 20 characters")
            return

        response = self.master.client.send_register(username, password)

        if response == wp.RESPONSE_CODE.REGISTER_SUCCESS:
            messagebox.showinfo("Register Successful", "Account created successfully!")
            self.master.switch_frame(HomePage)
        else:
            messagebox.showerror("Register Failed", "Account already exists")
