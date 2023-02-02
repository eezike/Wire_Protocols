import tkinter as tk
from tkinter import messagebox

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