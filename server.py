# Python program to implement server side of chat room.
import socket
import threading
import sqlite3

class Server:

	def __init__(self, port = 9999):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.clients = dict()

		# retreives IP on host computer
		self.HOST = socket.gethostname()

		# takes argument from command prompt as port number
		self.PORT = port

		self.current_users = dict()
	
	def bind(self):
		"""
		binds the server to an entered IP address and at the
		specified port number.
		The client must be aware of these parameters
		"""
		self.server.bind((self.HOST, self.PORT))
	
	def listen(self, listeners = 100):
		"""
		listens for 100 active clientsocketections. This number can be
		modified as per convenience.
		"""
		print(f"Listening on port {self.PORT}")
		self.server.listen(listeners)
		

	def run(self):

		self.bind()
		self.listen()

		while 1:
			"""Accepts a clientsocket request and stores two parameters,
			clientsocket which is a socket object for that user, and addr
			which contains the IP address of the client that just
			clientsocket"""
			clientsocket, addr = self.server.accept()

			self.current_users = []

			print(addr[0] + " has joined")

			threading.Thread(target = handle_client, args = (clientsocket, addr)).start()


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

