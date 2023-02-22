# Python program to implement server side of chat room.
import socket
import threading
import backend.database as database
from backend.service_classes import VERSION, HEADER_FORMAT, MESSAGE_TYPES, Message, SendMessageRequest, Response, GetUsersRequest, UsersStreamResponse, MessagesStreamResponse, LoginRequest, RegisterRequest, DeleteUserRequest, StreamEnd, Error, GetMessagesRequest, SingleMessageResponse, DeleteUserResponse, AddUserResponse
from backend.service import Stub
from collections import defaultdict
import queue

class Server:
	'''
	Server class than can accept client connections and respond to client requestions
	'''

	def __init__(self, port : int = 9999, max_clients : int = 10, name : str = None):

		# set up a socket server with specified parameters
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# retreives hostname on host computer
		self.HOST = socket.gethostname()

		# retreives IP on host computer
		self.IP = socket.gethostbyname(self.HOST)

		# takes argument from command prompt as port number
		self.PORT = port

		# initialize the sql database with the server
		self.db = database.Database(name)

		# dict that tracks an authenticated user to their associated client sockets: (username : str) -> (list[clientsocket : socket])
		self.authenticated_users = dict()

		# The max amount of users the server will accept
		self.MAX_CLIENTS = max_clients
	
		# create a thread-safe queue to buffer messages to be sent
		self.message_queue = defaultdict(queue.Queue)

	def send_in_queue(self, socket : socket):
		while True:
			message = self.message_queue[socket].get()
			if type(message) is list:
				Stub(socket).SendStream(message)
			else:
				Stub(socket).Send(message)
			self.message_queue[socket].task_done()

	
	def run(self):

		# binds the server to the host and port 
		self.server.bind((self.HOST, self.PORT))

		# starts listening for incoming client connections
		self.server.listen(self.MAX_CLIENTS)

		print("Server IP: ", self.IP)
		print(f"Listening on port {self.PORT}")

		while True:

			# accepts a client socket request
			clientsocket, addr = self.server.accept()
			print(addr[0] + " has joined")

			# start a new thread to handle the client connection
			threading.Thread(target = self.handle_client, args = (clientsocket, addr)).start()

	def handle_client(self, clientsocket: socket, addr : int) -> None:
		try:
			# Initialize variables
			username = None
			message_type_to_function = {
				MESSAGE_TYPES.SendMessageRequest : self.send_message,
				MESSAGE_TYPES.GetUsersRequest : self.get_users,
				MESSAGE_TYPES.DeleteUserRequest : self.delete_user,
				MESSAGE_TYPES.GetMessagesRequest : self.get_messages
			}

			# Create a client-side representation of the server
			stub = Stub(clientsocket)

			# Send a welcome message to the client
			response = Response(success=True, message= "Welcome to the chat service!")
			self.message_queue[clientsocket].put(response)

			# start a new thread to handle the client connection
			threading.Thread(target = self.send_in_queue, args = (clientsocket,)).start()

			# Loop forever
			while True:

				# Loop until the client is authenticated
				while True:
					username = self.authenticate(clientsocket, stub)
					if username:
						break

				# Loop to handle incoming messages from the client
				while username in self.authenticated_users:
					# Receive a message from the client
					message_type, payload = stub.Recv()

					# Check if the received message type is supported
					if message_type in message_type_to_function:
						# Call the appropriate function to handle the message
						message_type_to_function[message_type](message_type, payload, clientsocket)
					else:
						# Send an error response if the message type is not supported
						response = Response(success=False, message= "Unexpected message type")
						self.message_queue[clientsocket].put(response)
		
		except (ConnectionResetError, BrokenPipeError):
			# Print a message if the client disconnects unexpectedly
			print(addr[0] + ' disconnected unexpectedly')

		finally:
			# Close the client socket
			clientsocket.close()

			# Remove the client from the list of authenticated users if it was authenticated
			if username in self.authenticated_users:
				del self.authenticated_users[username]
			
			del self.message_queue[clientsocket]


				

	def authenticate(self, clientsocket: socket, stub: Stub) -> str:
		"""
		Authenticates a user via login/register. Returns the authenticated username if successful, else None.		
		"""

		# Receive the message from the client
		message_type, payload = stub.Recv()

		if message_type == MESSAGE_TYPES.LoginRequest:
			# If message is a LoginRequest
			try:
				# Try to login the user and add the clientsocket to authenticated_users dictionary
				loginreq : LoginRequest = stub.Parse(message_type, payload)
				self.db.login(loginreq.username, loginreq.password)

				self.authenticated_users[loginreq.username] = clientsocket

				# Send a successful response message
				response = Response(success=True, message= "Login Successful")
				self.message_queue[clientsocket].put(response)

				return loginreq.username
			except Exception as e:
				# Send an error response message
				response = Response(success=False, message= str(e))
				self.message_queue[clientsocket].put(response)

				return None

		elif message_type == MESSAGE_TYPES.RegisterRequest:
			# If message is a RegisterRequest
			try:
				# Try to register the user and add the clientsocket to authenticated_users dictionary
				registerreq : RegisterRequest = stub.Parse(message_type, payload)
				self.db.register(registerreq.username, registerreq.password)
				

				# Send a successful response message
				response = Response(success=True, message= "Registration Successful")
				self.message_queue[clientsocket].put(response)

				for other_socket in self.authenticated_users:
					response = AddUserResponse(username=registerreq.username)
					self.message_queue[other_socket].put(response)
				
				self.authenticated_users[registerreq.username] = clientsocket

				return registerreq.username
			except Exception as e:
				# Send an error response message
				response = Response(success=False, message= str(e))
				self.message_queue[clientsocket].put(response)

				return None

		else:
			# Send an error response message
			response = Response(success=False, message= "Unknown request sent; Authentication denied")
			self.message_queue[clientsocket].put(response)

			return None

		
	def send_message(self, message_type: int, payload: bytes, clientsocket: socket) -> None:
		try:
			# Parse the SendMessageRequest
			send_message_req: SendMessageRequest = Stub(clientsocket).Parse(message_type, payload)

			# Error if sending to user that doesn't exist:
			if send_message_req.recipient not in self.db.get_users():
				error = Error(message = "Recipient user does not exist!")
				self.message_queue[clientsocket].put(error)
				return
			

			# Check if the recipient is authenticated
			if send_message_req.recipient in self.authenticated_users:
				# Iterate over all the sockets belonging to the recipient
				other_socket = self.authenticated_users[send_message_req.recipient]
				# Create a response for each socket with the sender and content of the message
				single_message = SingleMessageResponse(sender=send_message_req.sender, content=send_message_req.content)
				self.message_queue[other_socket].put(single_message)
			else:
				# If recipient is not authenticated, save the message to the database
				self.db.save_message(sender=send_message_req.sender, recipient=send_message_req.recipient, content=send_message_req.content)

			response = Response(success=True, message="Single message sent")

		except:
			response = Response(success=False, message="Error sending message")

		# Send response back to the client
		self.message_queue[clientsocket].put(response)


	def get_users(self, message_type: int, payload: bytes, clientsocket: socket) -> None:
		# Parse the GetUsersRequest
		get_users_req: GetUsersRequest = Stub(clientsocket).Parse(message_type, payload)

		# Get the list of all users from the database
		users = self.db.get_users()

		# Create a response with the usernames of all authenticated users except the requesting user
		response = []
		for username in users:
			if username == get_users_req.username:
				continue
			response.append(UsersStreamResponse(username=username))

		# Send the response back to the client as a stream
		self.message_queue[clientsocket].put(response)


	def delete_user(self, message_type: int, payload: bytes, clientsocket: socket) -> None:

		# Parse the DeleteUserRequest
		delete_user_req: DeleteUserRequest = Stub(clientsocket).Parse(message_type, payload)

		try:
			# Delete the user from the database
			self.db.delete_user(delete_user_req.username)
		except:
			# If user does not exist in the database, send error message to client
			response = Response(success=False, message="User does not exist")
			self.message_queue[clientsocket].put(response)
			return

		# Inform all sockets that an account has been deleted
		for other_socket in self.authenticated_users:
			response = DeleteUserResponse(username=delete_user_req.username)
			self.message_queue[other_socket].put(response)
		

	def get_messages(self, message_type: int, payload: bytes, clientsocket: socket) -> None:
		# Parse the GetMessagesRequest object from the given payload
		get_messages_req : GetMessagesRequest = Stub(clientsocket).Parse(message_type, payload)

		# Retrieve the messages for the specified user from the database
		messages = self.db.get_messages(get_messages_req.username)

		# Create a list of MessagesStreamResponse objects for each message in the database
		response = []
		for sender, content in messages:
			response.append(MessagesStreamResponse(sender=sender, content=content))

		# Send the list of MessagesStreamResponse objects to the client
		self.message_queue[clientsocket].put(response)

if __name__ == "__main__":
    # Create a Server instance
    server = Server()

    # Start the server
    server.run()
