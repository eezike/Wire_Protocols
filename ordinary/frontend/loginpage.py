import tkinter as tk
from tkinter import messagebox
from backend.service import Response

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
        # Check if client is connected
        if self.master.client.connected == False:
            messagebox.showerror("Error", "Not connected")
            return

        # Get username and password from entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if username and password are not empty
        if len(username) == 0 or len(password) == 0:
            messagebox.showerror("Login Failed", "Username or password cannot be empty")
            return

        # Check if username and password are within the required length
        if len(username) > 20 or len(password) > 20:
            messagebox.showerror("Login Failed", "Invalid username or password")
            return

        # Try to login with the given username and password
        response : Response = self.master.client.login(username, password)

        # Check the server response
        if response.success:
            messagebox.showinfo("Login Successful", "Welcome " + username + "!")
            self.master.switch_frame(2)
        else:
            messagebox.showerror("Login Failed", response.message)

            
    def register(self):
        # Get username and password from entry fields
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Check if username and password are not empty
        if len(username) == 0 or len(password) == 0:
            messagebox.showerror("Register Failed", "Username or password cannot be empty")
            return

        # Check if username and password are within the required length
        elif len(username) > 20 or len(password) > 20:
            messagebox.showerror("Register Failed", "Username or password cannot exceed 20 characters")
            return

        # Try to register with the given username and password
        response : Response = self.master.client.register(username, password)

        # Check the server response
        if response.success:
            messagebox.showinfo("Register Successful", "Account created successfully!")
            self.master.switch_frame(2)
        else:
            messagebox.showerror("Register Failed", response.message)
