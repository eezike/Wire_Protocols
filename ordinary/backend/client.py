# dhcp-10-250-150-39.harvard.edu
# DESKTOP-EUAUCFM
# Victor: 10.250.235.165
# Emeka: 10.250.150.39
# Python program to implement client side of chat room.
import socket
from backend.service_classes import VERSION, HEADER_FORMAT, MESSAGE_TYPES, Message, SendMessageRequest, Response, GetUsersRequest, UsersStreamResponse, MessagesStreamResponse, LoginRequest, RegisterRequest, DeleteUserRequest, StreamEnd, Error, GetMessagesRequest, SingleMessageResponse
from backend.service import Stub


# Define the Client class
class Client:
    
    # Initialize the class and set some default properties
    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.username = None
        self.stub = Stub(self.clientsocket, client = True)
    
    # Connect to the specified host and port
    def connect(self, host="10.228.185.36", port=9999):
        # If not already connected, try to connect
        if not self.connected:
            try:
                self.clientsocket.connect((host, port))
                # Receive a response from the server and parse it
                message_type, payload = self.stub.Recv()
                response : Response = self.stub.Parse(message_type, payload)
                
                # If the response indicates success, set connected to True
                if response.success:
                    self.connected = True
            except:
                pass
        
        # Return the value of connected
        return self.connected
    
    # Log in to the chat server with the specified username and password
    def login(self, username, password) -> Response:
        # Create a LoginRequest object with the specified username and password
        request = LoginRequest(username= username, password= password)
        # Send the request to the server and parse the response
        response : Response = self.stub.Send(request)
        # Set the value of the username property
        self.username = username
        # Return the response
        return response
    
    # Register a new account with the specified username and password
    def register(self, username, password) -> Response:
        # Create a RegisterRequest object with the specified username and password
        request = RegisterRequest(username= username, password= password)
        # Send the request to the server and parse the response
        response : Response = self.stub.Send(request)
        # Set the value of the username property
        self.username = username
        # Return the response
        return response
    
    # Send a message to the specified recipient with the specified content
    def send_message(self, recipient, content) -> None:
        # Create a SendMessageRequest object with the sender username, recipient username, and message content
        request = SendMessageRequest(sender= self.username, recipient= recipient, content= content)
        # Send the request to the server
        self.stub.Send(request, recieve= False)

    # Get a list of users currently connected to the chat server
    def get_users(self) -> list[str]:
        # Create a GetUsersRequest object with the username of the current user
        request = GetUsersRequest(username = self.username)
        # Send the request to the server and parse the response, which is a list of UsersStreamResponse objects
        response : list[UsersStreamResponse] = self.stub.Send(request)
        # Extract the usernames from the UsersStreamResponse objects and return them as a list
        return [user.username for user in response]
    
    # Get a list of messages sent to the current user
    def get_messages(self) -> list[MessagesStreamResponse]:
        # Create a GetMessagesRequest object with the username of the current user
        request = GetMessagesRequest(username = self.username)
        # Send the request to the server and parse the response, which is a list of MessagesStreamResponse objects
        response : list[MessagesStreamResponse] = self.stub.Send(request)
        # Return the list of MessagesStreamResponse objects
        return response
    
    def delete_account(self) -> None:
        # create a request to delete the current user's account
        request = DeleteUserRequest(username=self.username)
        # send the request
        self.stub.Send(request, recieve= False)

        
    def listen_for_updates(self):
        # receive a message from the server
        message_type, payload = self.stub.Recv()
        response = self.stub.Parse(message_type, payload)

        return message_type, response
    
    def close(self):
        self.connected = False
        self.username = None
        self.clientsocket.close()