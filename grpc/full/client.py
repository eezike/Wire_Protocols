import grpc
import chat_service_pb2
import chat_service_pb2_grpc
import _thread

channel = grpc.insecure_channel('localhost:50051')
auth_stub = chat_service_pb2_grpc.AuthServiceStub(channel)
chat_stub = chat_service_pb2_grpc.ChatServiceStub(channel)

def run():
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
            response = auth_stub.Register(request)

            if response.success:
                print(response.message)
                break
            else:
                print(response.message)

def send_message():
    while True:
        print("\nMessaging Platform")



def receive_message():
    stream = auth_stub.ServerStreamingMethod(request)

    # Receive messages from the stream until there are no more.
    try:
        while True:
            # Receive the next message from the stream.
            response = stream.recv_message()
            
            # Process the received message as needed.
            print(response)
            
    except StopIteration:
        # The server has finished sending messages.
        pass

run()