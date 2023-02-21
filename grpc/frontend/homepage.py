import tkinter as tk
from tkinter import messagebox
import threading
import sys
 
class HomePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        # Exit boolean to stop receive messages thread
        self.receiving = True

        # Message list
        self.messages_list = tk.Listbox(self, height=15, width=50)
        self.messages_list.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # Options menu w/out current user
        self.options = self.master.client.get_users()

        # Current recipient in dropdown
        self.recipient = tk.StringVar()

        # Create dropdown with options 
        self.dropdown = tk.OptionMenu(self, self.recipient, *self.options, command=self.recipient_selected)
        self.dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Create message input
        self.message_input = tk.Text(self, height=3, width=30)
        self.message_input.grid(row=0, column=2, sticky="W", padx=10, pady=10)

        # Create send button
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, sticky="E", padx=10, pady=10)

        # Create reset option button
        self.reset_button = tk.Button(self, text="Reset Options", command=self.reset)
        self.reset_button.grid(row=1, column=2, sticky="E", padx=0, pady=0)

        # Create delete button
        self.delete_button = tk.Button(self, text="Delete Account", command=self.delete_account)
        self.delete_button.grid(row=2, column=2, sticky="E", padx=0, pady=0)

        # Recieve messages constantly in a thread
        threading.Thread(target = self.receive_messages).start()
    
    def send_message(self):
        """
        Send message to a recipient selected in the dropdown.
        """
        body = self.message_input.get("1.0", 'end-1c')

        # Msg error checking
        if len(body) == 0 or len(self.recipient.get()) == 0:
            messagebox.showerror("Message Send Failed", "Cannot send empty messages")
            return
        
        if self.recipient.get() == self.master.client.username:
            messagebox.showerror("Message Send Failed", "Cannot send messages to yourself")
            return
        
        # Send the message to the server and add it to our message list
        self.master.client.send_message(self.recipient.get(), body)
        self.add_message(self.recipient.get(), body)

        # Reset text input
        self.message_input.delete("1.0", tk.END)

    def receive_messages(self):
        """
        Receives messages and adds them to the inbox continuously.  
        """
        while True and self.receiving:
            messages = self.master.client.receive_messages()
            for message in messages:
                self.add_message(message.sender, message.content, True)

    def add_message(self, other, body, receiver = False):
        """
        Adds a message to the GUI's messagebox/listbox element
        """
        # Format msg differently for receivers & senders
        if receiver:
            self.messages_list.insert("end", f"{other}: {body}")
        else:
            self.messages_list.insert("end", f"You -> {other}: {body}")

    def delete_account(self):
        """
        Deletes the client's account from the server's database
        """
        result = messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            self.master.client.delete_account()

            # Destroy GUI and stop receiving messages
            self.receiving = False 
            self.master.destroy()

    def recipient_selected(self, *args):
        """
        Function needed for dropdown documentation
        """
        pass

    def reset(self):
        self.options = self.master.client.get_users()
        self.dropdown = tk.OptionMenu(self, self.recipient, *self.options, command=self.recipient_selected)
        self.dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.message_input.delete("1.0", tk.END)