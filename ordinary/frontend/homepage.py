import tkinter as tk
from tkinter import messagebox
from backend.service import MESSAGE_TYPES, MessagesStreamResponse
import threading

class HomePage(tk.Frame):
    def __init__(self, master):
        # Initialize the frame and set the master
        tk.Frame.__init__(self, master)
        self.master = master

        # Create the listbox to display the messages
        self.messages_list = tk.Listbox(self, height=15, width=50)
        self.messages_list.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # Create a StringVar to store the recipient
        self.recipient = tk.StringVar()

        # Get the list of available users and create an OptionMenu to select a recipient
        self.options = self.master.client.get_users()
        self.options = self.options if self.options else [" "]
        self.dropdown = tk.OptionMenu(self, self.recipient, *self.options)
        self.dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Create the input field for the message
        self.message_input = tk.Text(self, height=3, width=30)
        self.message_input.grid(row=0, column=2, sticky="W", padx=10, pady=10)

        # Create a button to send the message
        send_button = tk.Button(self, text="Send", command=self.send_message)
        send_button.grid(row=1, column=1, sticky="E", padx=10, pady=10)

        # Create a button to delete account
        delete_account_button = tk.Button(self, text="Delete Account", command=self.delete_account)
        delete_account_button.grid(row=1, column=2, sticky="E", padx=10, pady=10)

        # Display any messages that are already in the inbox
        self.get_inbox()

        # Start a new thread to listen for new messages
        threading.Thread(target=self.listen, daemon=True).start()

    def send_message(self):
        # Get the message content and check for errors
        content = self.message_input.get("1.0", 'end-1c').strip()

        if self.recipient.get().strip() == "" or content == "":
            # Display an error message if recipient or message is invalid
            messagebox.showerror("Error", "Invalid recipient or message")
            return
        if len(content) > 256:
            # Display an error message if message length is greater than 256 characters
            messagebox.showerror("Error", "Max message length of 256 characters")
            return
        if self.recipient.get() == self.master.client.username:
            # Display an error message if trying to send a message to oneself
            messagebox.showerror("Message Send Failed", "Cannot send messages to yourself")
            return

        # Send the message and add it to the listbox
        self.master.client.send_message(self.recipient.get(), content)


    def add_message(self, other, content, receiver=False):
        # Add a message to the listbox
        if receiver:
            self.messages_list.insert("end", f"{other}: {content}")
        else:
            self.messages_list.insert("end", f"You -> {other}: {content}")

    def get_inbox(self):
        # Get the messages in the inbox and display them in the listbox
        inbox : list[MessagesStreamResponse] = self.master.client.get_messages()
        for message in inbox:
            self.add_message(message.sender, message.content, True)

        # display no new messages if inbox empty
        if len(inbox) == 0:
            self.messages_list.insert("end", "NO NEW MESSAGES")
        
    def delete_account(self):
        self.master.client.delete_account()

    def listen(self):
        # Start listening for updates indefinitely
        while True:

            message_type, response = self.master.client.listen_for_updates()

            if message_type == MESSAGE_TYPES.SingleMessageResponse:
                # add incoming chat messages to view
                self.add_message(response.sender, response.content, True)
            elif message_type == MESSAGE_TYPES.Response:
                # show unsucessful response messages as errors
                if not response.success:
                    messagebox.showerror("Failure", response.message)
                else:
                    # add message to view only if response is successful
                    self.add_message(self.recipient.get(), self.message_input.get("1.0", 'end-1c').strip())
                    self.message_input.delete("1.0", tk.END)
            elif message_type == MESSAGE_TYPES.Error:
                # show errors
                messagebox.showerror("Error", response.message)
            elif message_type == MESSAGE_TYPES.AddUserResponse:
                # on new user registration, reinstantiate dropdown and add new user
                self.options.append(response.username)
                self.dropdown.destroy()
                self.dropdown = tk.OptionMenu(self, self.recipient, *self.options)
                self.dropdown.grid(row=0, column=1, padx=10, pady=10)
            elif message_type == MESSAGE_TYPES.DeleteUserResponse:
                if self.master.client.username == response.username:
                    # logout on self deletion
                    self.master.client.username = ""
                    self.master.switch_frame(1)
                    break
                else:
                    # on user deletion, reinstantiate dropdown and remove new user
                    if response.username in self.options:
                        self.options.remove(response.username)
                    self.dropdown.destroy()
                    self.recipient = tk.StringVar()
                    self.dropdown = tk.OptionMenu(self, self.recipient, *self.options)
                    self.dropdown.grid(row=0, column=1, padx=10, pady=10)
            else:
                # error if seeing anything else
                messagebox.showerror("Error", "Unhandled message type")
