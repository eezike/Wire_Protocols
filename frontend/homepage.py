import tkinter as tk
from tkinter import messagebox

class HomePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        self.messages_list = tk.Listbox(self, height=15, width=50)
        self.messages_list.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        self.recipient = tk.StringVar()

        self.options = self.master.client.get_users()
        self.dropdown = tk.OptionMenu(self, self.recipient, *self.options, command=self.recipient_selected)
        self.dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.message_input = tk.Text(self, height=3, width=30)
        self.message_input.grid(row=0, column=2, sticky="W", padx=10, pady=10)


        send_button = tk.Button(self, text="Send", command=self.send_message)
        send_button.grid(row=1, column=1, sticky="E", padx=10, pady=10)
    
    def send_message(self):
        pass
        # body = self.message_input.get("1.0", 'end-1c')

        # self.master.client.send_message(self.recipient, _from, body)
        
        # self.add_message(self.recipient, "You", body)
        
        # self.message_input.delete("1.0", tk.END)

    def add_message(self, _to, _from, body):
        self.messages_list.insert("end", f"{_from} -> {_to}: {body}")
        

    def recipient_selected(self, *args):
        pass
        # selected_option = self.recipient.get()
        # print(f"Recepient: {selected_option}")
    