# Python program to implement server side of chat room.
import socket
import threading


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# takes the first argument from command prompt as IP address
host = socket.gethostname()

# takes second argument from command prompt as port number
port = 9999

"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((host, port))

"""
listens for 100 active clientsocketections. This number can be
increased as per convenience.
"""
server.listen(100)

clients = dict()

def handle_client(clientsocket, addr):

	# sends a message to the client whose user object is clientsocket
	clientsocket.send("Welcome to this chatroom!".encode("ascii"))

	while True:
		try:
			message = clientsocket.recv(2048)
			if message:
				broadcast(message)

			else:
				"""message may have no content if the clientsocketection
				is broken, in this case we remove the clientsocketection"""
				remove(addr)

		except:
			continue

"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def broadcast(message):
	for addr, clientsocket in clients.items():
		try:
			clientsocket.send(message)
		except:
			clientsocket.close()

			# if the link is broken, we remove the client
			remove(addr)

def remove(addr):
	del clients[addr]

while True:

	"""Accepts a clientsocket request and stores two parameters,
	clientsocket which is a socket object for that user, and addr
	which contains the IP address of the client that just
	clientsocket"""
	clientsocket, addr = server.accept()

	
	clients[addr] = clientsocket

	# prints the address of the user that just clientsocket
	print(addr[0] + " has joined")

	# creates and individual thread for every user
	# that clientsocketects
	threading.Thread(target = handle_client, args = (clientsocket, addr)).start()

clientsocket.close()
server.close()
