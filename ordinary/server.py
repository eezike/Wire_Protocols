# Python program to implement server side of chat room.
import socket
import threading
import backend.database as database
from backend.service_classes import VERSION, HEADER_FORMAT, MESSAGE_TYPES, Message, SendMessageRequest, Response, GetUsersRequest, UsersStreamResponse, MessagesStreamResponse, LoginRequest, RegisterRequest, DeleteUserRequest, StreamEnd, Empty, GetMessagesRequest, SingleMessageResponse
from backend.service import Stub
from collections import defaultdict

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
		self.authenticated_users = defaultdict(list)

		# The max amount of users the server will accept
		self.MAX_CLIENTS = max_clients
	
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
			stub.Send(response)

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
						message_type_to_function[message_type](message_type, payload, stub)
					else:
						# Send an error response if the message type is not supported
						response = Response(success=False, message= "Unexpected message type")
						stub.Send(response)
		
		except (ConnectionResetError, BrokenPipeError):
			# Print a message if the client disconnects unexpectedly
			print(addr[0] + ' disconnected unexpectedly')

		finally:
			# Close the client socket
			clientsocket.close()

			# Remove the client from the list of authenticated users if it was authenticated
			if username in self.authenticated_users:
				self.authenticated_users[username].remove(clientsocket)


				

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

				self.authenticated_users[loginreq.username].append(clientsocket)

				# Send a successful response message
				response = Response(success=True, message= "Login Successful")
				stub.Send(response)

				return loginreq.username
			except Exception as e:
				# Send an error response message
				response = Response(success=False, message= str(e))
				stub.Send(response)

				return None

		elif message_type == MESSAGE_TYPES.RegisterRequest:
			# If message is a RegisterRequest
			try:
				# Try to register the user and add the clientsocket to authenticated_users dictionary
				registerreq : RegisterRequest = stub.Parse(message_type, payload)
				self.db.register(registerreq.username, registerreq.password)
				
				self.authenticated_users[registerreq.username].append(clientsocket)

				# Send a successful response message
				response = Response(success=True, message= "Registration Successful")
				stub.Send(response)

				return registerreq.username
			except Exception as e:
				# Send an error response message
				response = Response(success=False, message= str(e))
				stub.Send(response)

				return None

		else:
			# Send an error response message
			response = Response(success=False, message= "Unknown request sent; Authentication denied")
			stub.Send(response)

			return None

		
	def send_message(self, message_type: int, payload: bytes, stub: Stub) -> None:
		try:
			# Parse the SendMessageRequest
			send_message_req: SendMessageRequest = stub.Parse(message_type, payload)

			# Check if the recipient is authenticated
			if send_message_req.recipient in self.authenticated_users:
				# Iterate over all the sockets belonging to the recipient
				for socket in self.authenticated_users[send_message_req.recipient]:
					temp_stub = Stub(socket)
					# Create a response for each socket with the sender and content of the message
					single_message = SingleMessageResponse(sender=send_message_req.sender, content=send_message_req.content)
					temp_stub.Send(single_message)
			else:
				# If recipient is not authenticated, save the message to the database
				self.db.save_message(sender=send_message_req.sender, recipient=send_message_req.recipient, content=send_message_req.content)

			response = Response(success=True, message="Single message sent")

		except:
			response = SingleMessageResponse(sender=False, content="Error sending message")

		# Send response back to the client
		stub.Send(response)


	def get_users(self, message_type: int, payload: bytes, stub: Stub) -> None:
		# Parse the GetUsersRequest
		get_users_req: GetUsersRequest = stub.Parse(message_type, payload)

		# Get the list of all users from the database
		users = self.db.get_users()

		# Create a response with the usernames of all authenticated users except the requesting user
		response = []
		for username in users:
			if username == get_users_req.username:
				continue
			response.append(UsersStreamResponse(username=username))

		# Send the response back to the client as a stream
		stub.SendStream(response)


	def delete_user(self, message_type: int, payload: bytes, stub: Stub) -> None:
		# Parse the DeleteUserRequest
		delete_user_req: DeleteUserRequest = stub.Parse(message_type, payload)

		try:
			# Delete the user from the database
			self.db.delete_user(delete_user_req.username)
		except:
			# If user does not exist in the database, send error message to client
			response = Response(success=False, message="User does not exist")
			stub.Send(response)

		# Inform all sockets belonging to the deleted user that the account has been deleted
		for socket in self.authenticated_users[delete_user_req.username]:
			temp_stub = Stub(socket)
			response = Response(success=True, message="Account deleted")
			temp_stub.Send(response)

		# TODO: tell all users that a user is gone

		

	def get_messages(self, message_type: int, payload: bytes, stub: Stub) -> None:
		# Parse the GetMessagesRequest object from the given payload
		get_messages_req : GetMessagesRequest = stub.Parse(message_type, payload)

		# Retrieve the messages for the specified user from the database
		messages = self.db.get_messages(get_messages_req.username)

		# Create a list of MessagesStreamResponse objects for each message in the database
		response = []
		for sender, content in messages:
			response.append(MessagesStreamResponse(sender=sender, content=content))

		# Send the list of MessagesStreamResponse objects to the client
		stub.SendStream(response)

if __name__ == "__main__":
    # Create a Server instance
    server = Server()

    # Start the server
    server.run()
