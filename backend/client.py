# dhcp-10-250-150-39.harvard.edu
# DESKTOP-EUAUCFM
# Victor: 10.250.235.165
# Emeka: 10.250.150.39
# Python program to implement client side of chat room.
import socket
import select
import threading
import wireprotocol as wp

class Client:
    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self, host="10.228.185.36", port=9999):
        if not self.connected:
            try:
                self.clientsocket.connect((host, port))
                self.connected = True
            except:
                pass
        return self.connected

    def send_login(self, username, password):

        # username = input("Username: ")
        # password = input("Password: ")

        wp.send(self.clientsocket, wp.MSG_TYPES.LOGIN, username=username, password=password)

    def send_register(self, username, password):
        wp.send(self.clientsocket, wp.MSG_TYPES.REGISTER, username=username, password=password)

    def receive_messages(self):
        while True:
            message = self.clientsocket.recv(2048)
            if message:
                print(message.decode("ascii"))