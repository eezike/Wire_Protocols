import tkinter as tk
from tkinter import messagebox

class RegisterPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        # Create button to go back to login page
        tk.Button(self, text="Go Back", command=self.swtich_to_login).pack()

        # Create label for username
        self.username_label = tk.Label(self, text="Username:", font=("TkDefaultFont", 16))
        self.username_label.pack()
        
        # Create entry for username
        self.username_entry = tk.Entry(self, font=("TkDefaultFont", 14))
        self.username_entry.pack()
        self.username_entry.focus_set()
        
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
        elif self.master.db.register(username, password) == None:
            messagebox.showerror("Register Failed", "Account already exists")
        else:
            messagebox.showinfo("Register Successful", "Account created successfully!")
            self.swtich_to_login()

    def swtich_to_login(self):
        from frontend.loginpage import LoginPage
        self.master.switch_frame(LoginPage)