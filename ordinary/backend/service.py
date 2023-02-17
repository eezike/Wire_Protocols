import struct
import socket
from service_classes import VERSION, HEADER_FORMAT, MESSAGE_TYPES, Message, SendMessageRequest, Response, GetUsersRequest, UsersStreamResponse, MessagesStreamResponse, LoginRequest, RegisterRequest, DeleteUserRequest, StreamEnd, Empty, GetMessagesRequest, SingleMessageResponse

class Stub:
    def __init__(self, socket: socket, client : bool = False):
        self.socket = socket
        self.client = client

        self.single_message_types_to_class = {
            MESSAGE_TYPES.SendMessageRequest :  SendMessageRequest,
            MESSAGE_TYPES.Response :  Response,
            MESSAGE_TYPES.GetUsersRequest :  GetUsersRequest,
            MESSAGE_TYPES.LoginRequest :  LoginRequest,
            MESSAGE_TYPES.RegisterRequest :  RegisterRequest,
            MESSAGE_TYPES.DeleteUserRequest :  DeleteUserRequest,
            MESSAGE_TYPES.StreamEnd :  StreamEnd,
            MESSAGE_TYPES.Empty : Empty,
            MESSAGE_TYPES.GetMessagesRequest: GetMessagesRequest,
            MESSAGE_TYPES.SingleMessageResponse: SingleMessageResponse
        }

        self.stream_message_types_to_class = {
            MESSAGE_TYPES.UsersStreamResponse :  UsersStreamResponse,
            MESSAGE_TYPES.MessagesStreamResponse :  MessagesStreamResponse
        }


        
    def Send(self, request: Message, recieve = False) -> Message:
        binary_request = request.pack()
        self.socket.sendall(binary_request)

        if self.client or recieve:
            message_type, payload = self.Recv()
            print("Caught in send")
            return self.Parse(message_type, payload)
    
    def Recv(self) -> tuple[int, bytes]:
        """Receive a message from the socket"""
        header = self.socket.recv(struct.calcsize(HEADER_FORMAT))
        version, message_type, payload_size = struct.unpack(HEADER_FORMAT, header)
        if version != VERSION:
            print("Error: incorrect version #" + str(version))
            return None, None

        payload = self.socket.recv(payload_size)
        return message_type, payload
    
    def ParseStream(self, expected_message_type: int) -> list[Message]:
        class_type = self.stream_message_types_to_class[expected_message_type]
        for _ in range(100):
            message_type, payload = self.Recv()

            if message_type == MESSAGE_TYPES.StreamEnd:
                return []
            
            if message_type != expected_message_type:
                raise Exception(f"Unexpected message type {message_type} caught in stream for message type {expected_message_type}")
            
            return [class_type().unpack(payload)] + self.ParseStream(type)
    
    def Parse(self, message_type: int, payload: bytes) -> tuple[int, any]:

        if message_type in self.single_message_types_to_class:
            res = self.single_message_types_to_class[message_type]().unpack(payload)
        elif message_type in self.stream_message_types_to_class:
            class_type = self.stream_message_types_to_class[message_type]
            res = [class_type().unpack(payload)]
            res = res + self.ParseStream(class_type)
        else:
            res = Response(success= False, message= "Unknown message type")

        return res
