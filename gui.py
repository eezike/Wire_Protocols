import tkinter as tk
from tkinter import messagebox

class LoginFrame(tk.Frame):
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
    
    def login(self):
        host = self.host_entry.get()
        port = self.port_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == "1234":
            messagebox.showinfo("Login Successful", "Welcome Admin!")
            self.master.switch_frame(HomePage)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


class HomePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master
        
        tk.Label(self, text="Home Page").pack()
        tk.Button(self, text="Go Back", command=lambda: master.switch_frame(LoginFrame)).pack()


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.geometry("400x300")
        self.switch_frame(LoginFrame)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

app = Application()
app.mainloop()
