import grpc
import backend.chat_service_pb2 as chat_service_pb2
import backend.chat_service_pb2_grpc as chat_service_pb2_grpc

class Client:
    def __init__(self):
        # Connections
        self.channel = self.auth_stub = self.chat_stub = None
        self.connected = False

        # Current user logged in
        self.username = "" 

    def connect(self, host="localhost", port=50051):
        """
        Tries to connect to the server given the inputs: host IP and port. 
        Upon connection retrieves auth and chat stub from server's channel.

        Returns a boolean of the client's connections status. 
        """
        if not self.connected:
            try:
                self.channel = grpc.insecure_channel(host + ':' + str(port)) 
                self.auth_stub = chat_service_pb2_grpc.AuthServiceStub(self.channel)
                self.chat_stub = chat_service_pb2_grpc.ChatServiceStub(self.channel)
                self.connected = True
            except:
                raise Exception("Incorrect hostname or port")

        return self.connected

    def receive_messages(self):
        """
        Retrieve messages from the server/stub associated with our current user 
        """
        messageObjs = self.chat_stub.ReceiveMessage(chat_service_pb2.User(username = self.username))
        return messageObjs

    def send_message(self, recipient, content):
        """
        Sends a message (content) to the recipient.
        """
        # Create a message request
        request = chat_service_pb2.SendRequest(sender = self.username, recipient = recipient, content = content)
            
        # Send message to the server via stub
        self.chat_stub.SendMessage(request)

    def get_users(self):
        """
        Returns a list of usernames currently stored with the server's database. 
        """
        userObjs = self.chat_stub.GetUsers(chat_service_pb2.Empty()) 
        return [userObj.username for userObj in userObjs]

    def login(self, username, password):
        """
        Tries to login by checking credentials with the server. 

        Returns a response code representing login success/error. 
        """
        request = chat_service_pb2.LoginRequest(username=username, password=password)
        response = self.auth_stub.Login(request)

        # Sets global user given login success
        if response.success:
            self.username = username

        return response
    
    def delete_account(self):
        """
        Delete's the client's account from the server's database.
        """
        request = chat_service_pb2.DeleteRequest(username = self.username)
        response = self.auth_stub.Delete(request)
        return response

    def register(self, username, password):
        """
        Registers a user with the server's database with given credentials. 

        Returns a response code representing register success/error. 
        """
        request = chat_service_pb2.RegisterRequest(username=username, password=password)
        response = self.auth_stub.Register(request)

        # Sets global user given register success
        if response.success:
            self.username = username

        return response