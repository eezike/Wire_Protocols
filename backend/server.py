# Python program to implement server side of chat room.
import socket
import threading
import database
import wireprotocol as wp

class Server:

	def __init__(self, port = 9999, max_clients = 10):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.clients = dict()

		# retreives IP on host computer
		self.HOST = socket.gethostname()

		self.IP = socket.gethostbyname(self.HOST)
		print("Your IP: ", self.IP)

		# takes argument from command prompt as port number
		self.PORT = port

		# initialize the database with the server
		self.db = database.Database()

		self.current_sockets = dict()

		self.current_users = dict()

		# The max amount of users the server will accept
		self.max_clients = max_clients

	def run(self):

		self.server.bind((self.HOST, self.PORT))
		self.server.listen(self.max_clients)
		print(f"Listening on port {self.PORT}")

		while 1:
			# Accepts a client socket request
			clientsocket, addr = self.server.accept()
			self.current_sockets[addr] = clientsocket
			print(addr[0] + " has joined")
			threading.Thread(target = self.handle_client, args = (clientsocket, addr)).start()

	def handle_client(self, clientsocket, addr):

		# sends a message to the client whose user object is clientsocket
		clientsocket.send("Established connection to server".encode("ascii"))

		# loop until authenticated
		while not self.authenticate(self.clientsocket, addr):
			continue
		
		while True:
			message_type, payload = wp.receive_message(clientsocket)

	def authenticate(self, clientsocket, addr):
		"""
		Authenticates a user via login/register. Returns True if authenticated properly.		
		"""
		message_type, payload = wp.receive_message(clientsocket)
		if message_type == wp.MSG_TYPES.LOGIN:
			user, password = wp.unpack_payload(message_type, payload)
			if self.db.login(username, password) != None:
				# broadcast login success
				pass
			else:
				# broadcase login error
				pass
		elif message_type == wp.MSG_TYPES.REGISTER:
			username, password = wp.unpack_payload(message_type, payload)
			if self.db.register(username, password) != None:
				# wp.send(clientsocket, wp.)
				self.current_sockets[username] = clientsocket
				pass
			else:
				# broadcase register error
				pass
		else:
			# broadcast message_type error
			pass

		# Start chatroom

server = Server()
server.run()