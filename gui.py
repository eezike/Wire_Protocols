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
        self.host_label.grid(row=0, column=0, padx=10, pady=10)
        
        # Create entry for host
        self.host_entry = tk.Entry(self, font=("TkDefaultFont", 14))
        self.host_entry.grid(row=0, column=1, padx=10, pady=10)

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

        # Create button to go back to login page
        tk.Button(self, text="Go Back", command=lambda: master.switch_frame(LoginPage)).pack()

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
        elif db.register(username, password) == None:
            messagebox.showerror("Register Failed", "Account already exists")
        else:
            messagebox.showinfo("Register Successful", "Account created successfully!")
            self.master.switch_frame(LoginPage)

class HomePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        self.messages_list = tk.Listbox(self, height=15, width=50)
        self.messages_list.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        self.recipient = tk.StringVar()

        options = ["user1", "user2", "user3"]
        dropdown = tk.OptionMenu(self, self.recipient, *options, command=self.recipient_selected)
        dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.message_input = tk.Text(self, height=3, width=30)
        self.message_input.grid(row=0, column=2, sticky="W", padx=10, pady=10)


        send_button = tk.Button(self, text="Send", command=self.send_message)
        send_button.grid(row=1, column=1, sticky="E", padx=10, pady=10)
        
    
    def send_message(self):
        message = self.message_input.get("1.0", 'end-1c')
        self.messages_list.insert("end", "You: " + message)
        self.message_input.delete("1.0", tk.END)

    def recipient_selected(self, *args):
        selected_option = self.recipient.get()
        print(f"Recepient: {selected_option}")

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.geometry("400x350")
        self.switch_frame(LoginPage)
        # self.title("Chatroom")
        # self.geometry("850x300")
        # self.switch_frame(HomePage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

app = Application()
app.mainloop()
