# Python program to implement server side of chat room.
import socket
import threading
import backend.database as database
from backend.service_classes import VERSION, HEADER_FORMAT, MESSAGE_TYPES, Message, SendMessageRequest, Response, GetUsersRequest, UsersStreamResponse, MessagesStreamResponse, LoginRequest, RegisterRequest, DeleteUserRequest, StreamEnd, Empty, GetMessagesRequest, SingleMessageResponse
from backend.service import Stub
from collections import defaultdict

class Server:

	def __init__(self, port : int = 9999, max_clients : int = 10):

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# retreives IP on host computer
		self.HOST = socket.gethostname()

		self.IP = socket.gethostbyname(self.HOST)

		# takes argument from command prompt as port number
		self.PORT = port

		# initialize the database with the server
		self.db = database.Database()

		self.current_sockets = dict()

		self.authenticated_users = defaultdict(list)

		# The max amount of users the server will accept
		self.MAX_CLIENTS = max_clients
	
	def run(self):

		self.server.bind((self.HOST, self.PORT))
		self.server.listen(self.MAX_CLIENTS)
		print("Server IP: ", self.IP)
		print(f"Listening on port {self.PORT}")

		while True:
			# Accepts a client socket request
			clientsocket, addr = self.server.accept()
			self.current_sockets[addr] = clientsocket
			print(addr[0] + " has joined")
			threading.Thread(target = self.handle_client, args = (clientsocket, addr)).start()

	def handle_client(self, clientsocket: socket, addr : int) -> None:
		try:
			message_type_to_function = {
				MESSAGE_TYPES.SendMessageRequest : self.send_message,
				# MESSAGE_TYPES.Response : 0,
				MESSAGE_TYPES.GetUsersRequest : self.get_users,
				# MESSAGE_TYPES.UsersStreamResponse : 0,
				# MESSAGE_TYPES.MessagesStreamResponse : 0,
				# MESSAGE_TYPES.LoginRequest : 0,
				# MESSAGE_TYPES.RegisterRequest : 0,
				MESSAGE_TYPES.DeleteUserRequest : self.delete_user,
				# MESSAGE_TYPES.StreamEnd : 0,
				# MESSAGE_TYPES.Empty : 0,
				MESSAGE_TYPES.GetMessagesRequest : self.get_messages,
				# MESSAGE_TYPES.SingleMessageResponse : 0,
			}

			stub = Stub(clientsocket)
			# sends a message to the client whose user object is clientsocket
			response = Response(success=True, message= "Welcome to the chat service!")
			stub.Send(response)

			while True:

				# loop until authenticated
				while True:
					username = self.authenticate(clientsocket, stub)
					if username:
						break

				while username in self.authenticated_users:
					message_type, payload = stub.Recv()

					if message_type in message_type_to_function:
						message_type_to_function[message_type](message_type, payload, stub)
					else:
						# error
						response = Response(success=False, message= "Unexpected message type")
						stub.Send(response)
		
		except (ConnectionResetError, BrokenPipeError):
			print(addr[0] + ' disconnected unexpectedly')

		finally:
			clientsocket.close()
			if username in self.authenticated_users:
				self.authenticated_users[username].remove(clientsocket)
			del self.current_sockets[addr]

				

	def authenticate(self, clientsocket: socket, stub: Stub) -> str:
		"""
		Authenticates a user via login/register. Returns True if authenticated properly.		
		"""

		message_type, payload = stub.Recv()

		if message_type == MESSAGE_TYPES.LoginRequest:
			try:
				loginreq : LoginRequest = stub.Parse(message_type, payload)
				self.db.login(loginreq.username, loginreq.password)

				self.authenticated_users[loginreq.username].append(clientsocket)

				response = Response(success=True, message= "Login Successful")
				stub.Send(response)

				return loginreq.username
			except Exception as e:

				response = Response(success=False, message= str(e))
				stub.Send(response)

				return None


		elif message_type == MESSAGE_TYPES.RegisterRequest:	
			try:
				registerreq : RegisterRequest = stub.Parse(message_type, payload)
				self.db.register(registerreq.username, registerreq.password)
				
				self.authenticated_users[registerreq.username].append(clientsocket)

				response = Response(success=True, message= "Registration Successful")
				stub.Send(response)

				return registerreq.username
			except Exception as e:
				response = Response(success=False, message= str(e))
				stub.Send(response)

				return None

		else:
			# broadcast message_type error
			response = Response(success=False, message= "Unknown request sent; Authentication denied")
			stub.Send(response)

			return None
	
	def send_message(self, message_type: int, payload: bytes, stub: Stub) -> None:

		try:

			send_message_req : SendMessageRequest = stub.Parse(message_type, payload)

			if send_message_req.recipient in self.authenticated_users:
				for socket in self.authenticated_users[send_message_req.recipient]:
					temp_stub = Stub(socket)
					single_message = SingleMessageResponse(sender=send_message_req.sender, content=send_message_req.content)
					temp_stub.Send(single_message)
			else:
				self.db.save_message(sender=send_message_req.sender, recipient=send_message_req.recipient, content=send_message_req.content)
			
			response = Response(success=True, message="Single message sent")

		except:
			response = SingleMessageResponse(sender=False, content="Error sending message")
		
		stub.Send(response)

	def get_users(self, message_type: int, payload: bytes, stub: Stub) -> None:

		get_users_req : GetUsersRequest = stub.Parse(message_type, payload)

		users = self.db.get_users()

		response = []
		for username in users:
			if username == get_users_req.username:
				continue
			response.append(UsersStreamResponse(username = username))
		
		stub.SendStream(response)

	def delete_user(self, message_type: int, payload: bytes, stub: Stub) -> None:

		delete_user_req : DeleteUserRequest = stub.Parse(message_type, payload)

		try:
			self.db.delete_user(delete_user_req.username)
		except:
			response = Response(success=False, message= "User does not exist")
			stub.Send(response)
		
		for socket in self.authenticated_users[delete_user_req.username]:
			temp_stub = Stub(socket)
			response = Response(success=True, message= "Account deleted")
			temp_stub.Send(response)
		
		# TODO: tell all users that a user is gone
		

	def get_messages(self, message_type: int, payload: bytes, stub: Stub) -> None:

		get_messages_req : GetMessagesRequest = stub.Parse(message_type, payload)

		messages = self.db.get_messages(get_messages_req.username)

		response = []
		for sender, content in messages:
			response.append(MessagesStreamResponse(sender=sender, content=content))
		
		print(response)
		stub.SendStream(response)



server = Server()
server.run()