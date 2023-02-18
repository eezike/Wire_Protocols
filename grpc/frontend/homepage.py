import tkinter as tk
from tkinter import messagebox
import threading

class HomePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        # Message list
        self.messages_list = tk.Listbox(self, height=15, width=50)
        self.messages_list.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # Options menu w/out current user
        self.options = self.master.client.get_users()
        self.options.remove(self.master.client.username)

        # Current recipient in dropdown
        self.recipient = tk.StringVar()

        # Create dropdown with options 
        self.dropdown = tk.OptionMenu(self, self.recipient, *self.options, command=self.recipient_selected)
        self.dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Create message input
        self.message_input = tk.Text(self, height=3, width=30)
        self.message_input.grid(row=0, column=2, sticky="W", padx=10, pady=10)

        # Create send button
        send_button = tk.Button(self, text="Send", command=self.send_message)
        send_button.grid(row=1, column=1, sticky="E", padx=10, pady=10)

        # 
        threading.Thread(target = self.receive_messages).start()
    
    def send_message(self):
        body = self.message_input.get("1.0", 'end-1c')
        if len(body) == 0 or len(self.recipient.get()) == 0:
            messagebox.showerror("Message Send Failed", "Cannot send empty messages")
        elif self.recipient.get() == self.master.client.username:
            messagebox.showerror("Message Send Failed", "Cannot send messages to yourself")
        else:
            self.master.client.send_message(self.recipient.get(), body)
            self.add_message(self.recipient.get(), "You", body)

        self.message_input.delete("1.0", tk.END)

    def receive_messages(self):
        """
        """
        while True:
            messages = self.master.client.receive_messages()
            for message in messages:
                self.add_message("You", message.sender, message.content)


    def add_message(self, sender, recipient, body):
        """
        
        """
        self.messages_list.insert("end", f"{sender} -> {recipient}: {body}")

    # def recipient_selected(self, *args):
    #     pass
    #     # selected_option = self.recipient.get()
    #     # print(f"Recepient: {selected_option}")
    