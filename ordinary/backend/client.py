# dhcp-10-250-150-39.harvard.edu
# DESKTOP-EUAUCFM
# Victor: 10.250.235.165
# Emeka: 10.250.150.39
# Python program to implement client side of chat room.
import socket
from service_classes import VERSION, HEADER_FORMAT, MESSAGE_TYPES, Message, SendMessageRequest, Response, GetUsersRequest, UsersStreamResponse, MessagesStreamResponse, LoginRequest, RegisterRequest, DeleteUserRequest, StreamEnd, Empty, GetMessagesRequest, SingleMessageResponse
from service import Stub


class Client:
    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.username = None
        self.stub = Stub(self.clientsocket, client = True)

    def connect(self, host="10.228.185.36", port=9999):
        if not self.connected:
            try:
                self.clientsocket.connect((host, port))
                response = self.stub.Send(Empty())
                if response.success:
                    self.connected = True
            except:
                pass

        return self.connected

    def Login(self, username, password) -> Response:
        request = LoginRequest(username= username, password= password)
        response = self.stub.Send(request)
        self.username = username
        return response

    def Register(self, username, password) -> Response:
        request = RegisterRequest(username= username, password= password)
        response = self.stub.Send(request)
        self.username = username
        return response
    
    def SendMessage(self, recipient, content) -> Response:
        request = SendMessageRequest(sender= self.username, recipient= recipient, content= content)
        response = self.stub.Send(request)
        return response
    
    def GetUsers(self) -> list[UsersStreamResponse]:
        request = GetUsersRequest(username = self.username)
        response = self.stub.Send(request)
        return response
    
    def GetMessages(self) -> list[MessagesStreamResponse]:
        request = GetMessagesRequest(username = self.username)
        response = self.stub.Send(request)
        return response
    
    def DeleteAccount(self) -> Response:
        request = DeleteUserRequest(username = self.username)
        response = self.stub.Send(request)
        return response
    
    def ListenForMessages(self, callback):
        while True:
            message_type, payload = self.stub.Recv()

            if message_type == MESSAGE_TYPES.SingleMessageResponse:
                chat_message = self.stub.Parse(message_type, payload)
                callback(chat_message)


        