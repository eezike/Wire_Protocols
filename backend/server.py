# Python program to implement server side of chat room.
import socket
import threading
import backend.database as database

class Server:

	def __init__(self, port = 9999):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.clients = dict()

		# retreives IP on host computer
		self.HOST = socket.gethostname()

		# takes argument from command prompt as port number
		self.PORT = port

		# initialize the database with the server
		self.db = database.Database()

		self.current_users = dict()
		
	def run(self):

		self.server.bind((self.HOST, self.PORT))
		self.server.listen(10)
		print(f"Listening on port {self.PORT}")

		while 1:
			"""Accepts a clientsocket request and stores two parameters,
			clientsocket which is a socket object for that user, and addr
			which contains the IP address of the client that just
			clientsocket"""
			clientsocket, addr = self.server.accept()

			self.current_users[addr] = {"socket": clientsocket, "username": None}

			print(addr[0] + " has joined")

			# 
			threading.Thread(target = self.authenticate, args = (clientsocket, addr)).start()

def authenticate(self, clientsocket, addr):
	# Check if user is logging in or registering
	pass
	# blah blah wire protocol blah blah got user name and password and register/login type already

	username = ""
	password = ""
	message_type = 0

	if message_type == 



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

clientsocket.close()

