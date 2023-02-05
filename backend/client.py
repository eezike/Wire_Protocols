# dhcp-10-250-150-39.harvard.edu
# DESKTOP-EUAUCFM
# Victor: 10.250.235.165
# Emeka: 10.250.150.39
# Python program to implement client side of chat room.
import socket
import select
import threading
from wireprotocol as wp

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "10.250.150.39"
port = 9999
client.connect((host, port))

name = input("Name: ")


def send_info():

    username = input("Username: ")
    password = input("Password: ")

    wp.send(client, wp.MSG_TYPES.LOGIN, username=username, password=password)
    
    # client.close()

def receive_info():
    while True:
        message = client.recv(2048)
        if message:
            print(message.decode("ascii"))

threading.Thread(target= send_info).start()
threading.Thread(target= receive_info).start()