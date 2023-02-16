import grpc
import chat_service_pb2
import chat_service_pb2_grpc
import threading

channel = grpc.insecure_channel('localhost:50051')
auth_stub = chat_service_pb2_grpc.AuthServiceStub(channel)
chat_stub = chat_service_pb2_grpc.ChatServiceStub(channel)

username = ""

def receive_messages():
    global username

    while True:
        messageObjs = chat_stub.ReceiveMessage(chat_service_pb2.User(username = username))
        for messageObj in messageObjs:
            response = f"{messageObj.sender}: {messageObj.content}"
            print(f"\nNew Message:\n{response}\n")

def send_messages():
    global username

    while True:
        print("\nMessaging")
        recipient = input("Recipient: ")
        content = input("Content: ")

        request = chat_service_pb2.SendRequest(sender = username, recipient = recipient, content = content)
        chat_stub.SendMessage(request)


def home():
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

    threading.Thread(target = send_messages).start()
    threading.Thread(target = receive_messages).start()
    


def login():
    global username
    while True:

        choice = input("\nRegister or Login: ")
        
        if "r" in choice.lower() :
            print("\nRegister")
            username = input("Username: ")
            password = input("Password: ")
            request = chat_service_pb2.RegisterRequest(username=username, password=password)
            response = auth_stub.Register(request)

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
            response = auth_stub.Login(request)

            if response.success:
                print(response.message)
                break
            else:
                print(response.message)

login()
home()