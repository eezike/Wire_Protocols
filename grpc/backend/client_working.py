import grpc
import chat_service_pb2
import chat_service_pb2_grpc
import threading

IP = 'localhost'
PORT = '50051'

class Client():
    def __init__(self):
        # Creating a channel to the server
        self.channel = grpc.insecure_channel(IP + ':' + PORT) 

        # Retrieve the auth and chat stubs in the server channel
        self.auth_stub = chat_service_pb2_grpc.AuthServiceStub(self.channel)
        self.chat_stub = chat_service_pb2_grpc.ChatServiceStub(self.channel)

        # Store logged in user
        username = ""

    def receive_messages(self):
        """
        Receives messages indefinitely from chat_stub. (run within thread)
        """
        while True:
            # Retrieve messages from the server/stub associated with our current user
            messageObjs = self.chat_stub.ReceiveMessage(chat_service_pb2.User(username = self.username))

            # Print all messages
            for messageObj in messageObjs:
                response = f"{messageObj.sender}: {messageObj.content}"
                print(f"\nNew Message:\n{response}\n")

    def send_messages(self):
        """
        Requests input indefinitely in order to send messages. (run within thread)
        """
        while True:
            # Request message recipient and content from client via command prompt
            print("\nMessaging")
            recipient = input("Recipient: ")
            content = input("Content: ")

            # Create a message request
            request = chat_service_pb2.SendRequest(sender = self.username, 
                                                recipient = recipient, 
                                                content = content)
            
            # Send message to the server via stub
            self.chat_stub.SendMessage(request)


    def home():
        """
        Chat application's home page (post-login)
        """
        global username
        
        print("\nHome")

        print("\nInbox:")
        messageObjs = chat_stub.ReceiveMessage(chat_service_pb2.User(username = username))
        no_messages = True
        for messageObj in messageObjs:
            print(f"{messageObj.sender}: {messageObj.content}")
            no_messages = False
        if no_messages:
            print("Empty")
        
        # Get users
        users = []
        userObjs = chat_stub.GetUsers(chat_service_pb2.Empty())

        for userObj in userObjs:
            users.append(userObj.username)

        print("\nUsers: ", users)

        # Simultaneously send and receive in separate threads
        threading.Thread(target = send_messages).start()
        threading.Thread(target = receive_messages).start()
        

    def login(self):
        """
        Login authentication
        """
        global username

        # Loop until user is authenticated
        while True:

            choice = input("\nRegister or Login: ")
            
            if "r" in choice.lower() :
                print("\nRegister")
                username = input("Username: ")
                password = input("Password: ")
                request = chat_service_pb2.RegisterRequest(username=username, password=password)
                response = self.auth_stub.Register(request)

                if response.success:
                    print(response.message)
                    break
                else:
                    print(response.message)
            else:
                print("\nLogin")
                username = input("Username: ")
                password = input("Password: ")
                request = chat_service_pb2.LoginRequest(username=username, password=password)
                response = self.auth_stub.Login(request)

                if response.success:
                    print(response.message)
                    break
                else:
                    print(response.message)
            

login()
home()