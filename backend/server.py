# Python program to implement server side of chat room.
import socket
import threading
import database
from wireprotocol as wp

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

		self.current_sockets = dict()
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

			self.current_sockets[addr] = clientsocket

			print(addr[0] + " has joined")

			threading.Thread(target = self.authenticate, args = (clientsocket, addr)).start()
	
	def authenticate(self, clientsocket, addr):
		message_type, payload = wp.receive_message(clientsocket)
		if message_type == wp.MSG_TYPES.LOGIN:
			user, password = wp.unpack_payload(message_type, payload)

			if self.db.login(username, password) != None:
				# broadcast login success
			else:
				# broadcase login error

		elif message_type == wp.MSG_TYPES.REGISTER:
			username, password = wp.unpack_payload(message_type, payload)

			if self.db.register(username, password) != None:
				wp.send(clientsocket, wp.)
				self.current_sockets[username] = clientsocket
			else:
				# broadcase register error
		else:
			# broadcast 
			pass

	def handle_client(self, clientsocket, addr):

		# sends a message to the client whose user object is clientsocket
		clientsocket.send("Welcome to this chatroom!".encode("ascii"))

		while True:
			try:

				message_type, payload = wp.receive_message(clientsocket)
				user, password = wp.unpack_payload(message_type, payload)

				print(user, password)
				


			except:
				continue

server = Server()
server.run()