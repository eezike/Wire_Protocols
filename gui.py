import tkinter as tk
from tkinter import messagebox
import database

db = database.Database()

class LoginPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        # Create label for host
        self.host_label = tk.Label(self, text="Host:", font=("TkDefaultFont", 16))
        self.host_label.pack()
        
        # Create entry for host
        self.host_entry = tk.Entry(self, font=("TkDefaultFont", 14))
        self.host_entry.pack()

        # Create label for port
        self.port_label = tk.Label(self, text="Port:", font=("TkDefaultFont", 16))
        self.port_label.pack()
        
        # Create entry for port
        self.port_entry = tk.Entry(self, font=("TkDefaultFont", 14))
        self.port_entry.pack()
        
        # Create label for username
        self.username_label = tk.Label(self, text="Username:", font=("TkDefaultFont", 16))
        self.username_label.pack()
        
        # Create entry for username
        self.username_entry = tk.Entry(self, font=("TkDefaultFont", 14))
        self.username_entry.pack()
        
        # Create label for password
        self.password_label = tk.Label(self, text="Password:", font=("TkDefaultFont", 16))
        self.password_label.pack()
        
        # Create entry for password
        self.password_entry = tk.Entry(self, font=("TkDefaultFont", 14), show="*")
        self.password_entry.pack()
        
        # Create login button
        self.login_button = tk.Button(self, text="Login", font=("TkDefaultFont", 14), command=self.login)
        self.login_button.pack()

        # Create register label
        self.register_label = tk.Label(self, text="Don't have an account?", font=("TkDefaultFont", 16))
        self.register_label.pack()

        # Create register button
        self.register_button = tk.Button(self, text="Register", font=("TkDefaultFont", 14), command=self.register)
        self.register_button.pack()
    
    def login(self):
        host = self.host_entry.get()
        port = self.port_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if db.login(username, password) == None:
            messagebox.showerror("Login Failed", "Invalid username or password")
        else:
            messagebox.showinfo("Login Successful", "Welcome " + username + "!")
            self.master.switch_frame(HomePage)

    def register(self):
        self.master.switch_frame(RegisterPage)

class RegisterPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        # Create label for username
        self.username_label = tk.Label(self, text="Username:", font=("TkDefaultFont", 16))
        self.username_label.pack()
        
        # Create entry for username
        self.username_entry = tk.Entry(self, font=("TkDefaultFont", 14))
        self.username_entry.pack()
        
        # Create label for password
        self.password_label = tk.Label(self, text="Password:", font=("TkDefaultFont", 16))
        self.password_label.pack()
        
        # Create entry for password
        self.password_entry = tk.Entry(self, font=("TkDefaultFont", 14), show="*")
        self.password_entry.pack()
        
        # Create login button
        self.register_button = tk.Button(self, text="Create Account", font=("TkDefaultFont", 14), command=self.register)
        self.register_button.pack()

    def register(self):
        # Retrieve entries 
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if input is valid
        if len(username) == 0 or len(password) == 0:
            messagebox.showerror("Register Failed", "Username or password cannot be empty")

        # Try to add account to database
        # TODO: should we make a global database instance?
        if db.register(username, password) == None:
            messagebox.showerror("Register Failed", "Account already exists")

        messagebox.showinfo("Register Successful", "Account created successfully!")
        self.master.switch_frame(LoginPage)

class HomePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master
        
        tk.Label(self, text="Home Page").pack()
        tk.Button(self, text="Go Back", command=lambda: master.switch_frame(LoginPage)).pack()

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.geometry("400x350")
        self.switch_frame(LoginPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

app = Application()
app.mainloop()
