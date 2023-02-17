# Python program to implement server side of chat room.
import socket
import threading
import database
from service_classes import VERSION, HEADER_FORMAT, MESSAGE_TYPES, Message, SendMessageRequest, Response, GetUsersRequest, UsersStreamResponse, MessagesStreamResponse, LoginRequest, RegisterRequest, DeleteUserRequest, StreamEnd, Empty, GetMessagesRequest, SingleMessageResponse
from service import Stub
from collections import defaultdict

class Server:

	def __init__(self, port : int = 9999, max_clients : int = 10):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		# retreives IP on host computer
		self.HOST = socket.gethostname()

		self.IP = socket.gethostbyname(self.HOST)
		print("Your IP: ", self.IP)

		# takes argument from command prompt as port number
		self.PORT = port

		# initialize the database with the server
		self.db = database.Database()

		self.current_sockets = dict()

		self.authenticated_users = defaultdict()

		# The max amount of users the server will accept
		self.MAX_CLIENTS = max_clients
	
	def val_error_code(self, response_code):
		try:
			response_code = response_code.args[1]
		except:
			response_code = wp.RESPONSE_CODE.UNKNOWN_ERROR
		return response_code

	def run(self):

		self.server.bind((self.HOST, self.PORT))
		self.server.listen(self.MAX_CLIENTS)
		print(f"Listening on port {self.PORT}")

		while True:
			# Accepts a client socket request
			clientsocket, addr = self.server.accept()
			self.current_sockets[addr] = clientsocket
			print(addr[0] + " has joined")
			threading.Thread(target = self.handle_client, args = (clientsocket, addr)).start()

	def handle_client(self, clientsocket: socket, addr : int):

		stub = Stub(clientsocket)
		# sends a message to the client whose user object is clientsocket
		response = Response(success=True, message= "Welcome to the chat service!")
		stub.Send(response)

		# loop until authenticated
		while True:
			username = self.authenticate(clientsocket, stub)
			if username:
				break
		
		message_type, payload = wp.receive_message(clientsocket)

		if message_type == wp.MSG_TYPES.RESPONSE:
			self.handle_response(clientsocket, payload)
		elif message_type == wp.MSG_TYPES.SEND_MSG:
			_to, _from, body = wp.unpack_payload(message_type, payload)

			if _to in self.current_users:
				wp.sendone(
					socket = self.current_users[_to],
					message_type = wp.MSG_TYPES.RES_MSGS,
					_to = _to,
					_from = _from,
					body = body
				)

				wp.sendone(
					socket = self.current_users[_to],
					message_type = wp.MSG_TYPES.RES_MSGS,
					_to = "",
					_from = "",
					body = ""
				)
			
			
	def handle_response(self, clientsocket : socket, payload : bytes):
		users = self.db.get_users()

		for user in users:
			wp.sendone(
				clientsocket, 
				wp.MSG_TYPES.RES_USERS,
				user = user)

		wp.sendone(
			clientsocket, 
			wp.MSG_TYPES.RES_USERS,
			user = "")
				

	def authenticate(self, clientsocket: socket, stub: Stub) -> str:
		"""
		Authenticates a user via login/register. Returns True if authenticated properly.		
		"""

		message_type, payload = stub.Recv()

		if message_type == MESSAGE_TYPES.LoginRequest:
			try:
				loginreq = stub.Parse(message_type, payload)
				self.db.login(username, password)
				response = Response(success=True, message= "Welcome to the chat service!")
				stub.Send(response)
				self.authenticated_users[username].append(clientsocket)
				return username
			except Exception as e:
				wp.sendone(
					socket = clientsocket, 
					message_type = wp.MSG_TYPES.RESPONSE, 
					response_code = self.val_error_code(e))
				return None


		elif message_type == MESSAGE_TYPES.RegisterRequest:	
			try:
				username, password = wp.unpack_payload(message_type, payload)
				self.db.register(username, password)
				wp.sendone(
					socket = clientsocket,
					message_type = wp.MSG_TYPES.RESPONSE,
					response_code = wp.RESPONSE_CODE.REGISTER_SUCCESS)
				self.current_users[username] = clientsocket
				return username
			except Exception as response_code:
				wp.sendone(
					socket = clientsocket,
					message_type = wp.MSG_TYPES.RESPONSE,
					response_code = self.val_error_code(response_code))
				return None
		else:
			# broadcast message_type error
			wp.sendone(
				socket = clientsocket, 
				message_type = wp.MSG_TYPES.RESPONSE, 
				response_code = wp.RESPONSE_CODE.UNKNOWN_ERROR)
			return None


server = Server()
server.run()