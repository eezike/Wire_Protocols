import tkinter as tk
from tkinter import messagebox
from backend.service_classes import MessagesStreamResponse, SingleMessageResponse
import threading

class HomePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        self.messages_list = tk.Listbox(self, height=15, width=50)
        self.messages_list.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        self.recipient = tk.StringVar()

        
        self.options = self.master.client.get_users()
        self.options = self.options if self.options else [" "]
        self.dropdown = tk.OptionMenu(self, self.recipient, *self.options)
        self.dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.message_input = tk.Text(self, height=3, width=30)
        self.message_input.grid(row=0, column=2, sticky="W", padx=10, pady=10)

        send_button = tk.Button(self, text="Send", command=self.send_message)
        send_button.grid(row=1, column=1, sticky="E", padx=10, pady=10)

        self.get_inbox()
        threading.Thread(target = self.listen).start()
    
    def send_message(self):
        
        content = self.message_input.get("1.0", 'end-1c')

        if self.recipient.get() == " " or content.strip() == "":
            messagebox.showerror("Error", "Invalid recipient or message")
            return 
        
        if len(content) > 256:
            messagebox.showerror("Error", "Max message length of 256 characters")
            return
        
        if self.recipient.get() == self.master.client.username:
            messagebox.showerror("Message Send Failed", "Cannot send messages to yourself")
            return

        self.master.client.send_message(self.recipient.get(), content)
        self.add_message(self.recipient.get(), content)
        self.message_input.delete("1.0", tk.END)

    def add_message(self, other, content, receiver = False):
        if receiver:
            self.messages_list.insert("end", f"{other}: {content}")
        else:
            self.messages_list.insert("end", f"You -> {other}: {content}")
        
    def get_inbox(self):
        inbox : list[MessagesStreamResponse] = self.master.client.get_messages()
        for message in inbox:
            self.add_message(message.sender, message.content, True)

        if len(inbox) == 0:
            self.messages_list.insert("end", "NO NEW MESSAGES")
        
    
    def listen(self):
        def callback(message: SingleMessageResponse):
            self.add_message(self, message.sender, message.content, True)
            
        self.master.client.listen_for_updates(callback)