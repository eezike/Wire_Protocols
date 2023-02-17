import grpc
import backend.chat_service_pb2 as chat_service_pb2
import backend.chat_service_pb2_grpc as chat_service_pb2_grpc
import threading

class Client:
    def __init__(self):
        # # Creating a channel to the server
        # self.channel = grpc.insecure_channel(IP + ':' + PORT) 

        # # Retrieve the auth and chat stubs in the server channel
        # self.auth_stub = chat_service_pb2_grpc.AuthServiceStub(self.channel)
        # self.chat_stub = chat_service_pb2_grpc.ChatServiceStub(self.channel)
        self.channel = self.auth_stub = self.chat_stub = None
        self.connected = False

        # Store logged in user
        self.username = ""

    def connect(self, host="10.228.185.36", port=50051):
        if not self.connected:
            try:
                self.channel = grpc.insecure_channel(host + ':' + str(port)) 
                self.auth_stub = chat_service_pb2_grpc.AuthServiceStub(self.channel)
                self.chat_stub = chat_service_pb2_grpc.ChatServiceStub(self.channel)
                self.connected = True
            except:
                pass

        return self.connected

    def receive_messages(self):
        """
        Receives messages indefinitely from chat_stub. (run within thread)
        """
        
        # Retrieve messages from the server/stub associated with our current user
        messageObjs = self.chat_stub.ReceiveMessage(chat_service_pb2.User(username = self.username))
        return messageObjs


    def send_message(self, recipient, content):
        """
        Requests input indefinitely in order to send messages. (run within thread)
        """


        # Create a message request
        print(self.username, recipient, content)
        request = chat_service_pb2.SendRequest(sender = self.username, recipient = recipient, content = content)
            
        # Send message to the server via stub
        self.chat_stub.SendMessage(request)

    def get_users(self):
        users = []
        userObjs = self.chat_stub.GetUsers(chat_service_pb2.Empty())

        for userObj in userObjs:
            users.append(userObj.username)
        
        return users

    # def home():
    #     """
    #     Chat application's home page (post-login)
    #     """
    #     global username
        
    #     print("\nHome")

    #     print("\nInbox:")
    #     messageObjs = chat_stub.ReceiveMessage(chat_service_pb2.User(username = username))
    #     no_messages = True
    #     for messageObj in messageObjs:
    #         print(f"{messageObj.sender}: {messageObj.content}")
    #         no_messages = False
    #     if no_messages:
    #         print("Empty")
        
    #     # Get users
    #     users = []
    #     userObjs = chat_stub.GetUsers(chat_service_pb2.Empty())

    #     for userObj in userObjs:
    #         users.append(userObj.username)

    #     print("\nUsers: ", users)

    #     # Simultaneously send and receive in separate threads
    #     threading.Thread(target = self.send_messages).start()
    #     threading.Thread(target = self.receive_messages).start()
        

    def login(self, username, password):
        request = chat_service_pb2.LoginRequest(username=username, password=password)
        response = self.auth_stub.Login(request)

        if response.success:
            self.username = username

        return response
    
    def register(self, username, password):
        request = chat_service_pb2.RegisterRequest(username=username, password=password)
        response = self.auth_stub.Register(request)

        if response.success:
            self.username = username

        return response