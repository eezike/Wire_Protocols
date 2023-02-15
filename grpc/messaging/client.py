import grpc

import chat_service_pb2
import chat_service_pb2_grpc

class ChatClient:
    def __init__(self, username):
        self.username = username
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = chat_service_pb2_grpc.ChatServiceStub(self.channel)
        self.join_chat()

    def join_chat(self):
        join_request = chat_service_pb2.JoinRequest(username=self.username)
        self.stream = self.stub.JoinChat(join_request)

    def send_message(self, recipient_username, message):
        message_request = chat_service_pb2.MessageRequest(sender_username=self.username, recipient_username=recipient_username, content=message)
        self.stub.SendMessage(message_request)

    def receive_messages(self):
        for message in self.stream:
            print(f"[{message.sender_username}] {message.content}")

if __name__ == '__main__':
    username = input("Enter a username: ")
    client = ChatClient(username)
    recipient_username = input("Enter the username of the person you want to send a message to: ")
    while True:
        message = input("Enter a message: ")
        client.send_message(recipient_username, message)
        client.receive_messages()
