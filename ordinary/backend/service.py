import struct
from service_classes import VERSION, HEADER_FORMAT, MESSAGE_TYPES, Message, SendRequest, Response, Empty, ChatMessage, User, LoginRequest, RegisterRequest


class Stub:
    def __init__(self, socket):
        self.socket = socket
        
    def Send(self, request: Message):
        binary_request = request.pack()
        self.socket.sendall(binary_request)
    
    def Recv(self) -> tuple[int, bytes]:
        """Receive a message from the socket"""
        header = self.socket.recv(struct.calcsize(HEADER_FORMAT))
        version, message_type, payload_size = struct.unpack(HEADER_FORMAT, header)
        if version != VERSION:
            print("Error: incorrect version #" + str(version))
            return None, None

        payload = self.socket.recv(payload_size)
        return message_type, payload
    
    def ReadStream(self, type: Message):
        for _ in range(100):
            message_type, payload = self.Recv()

            if message_type == MESSAGE_TYPES.StreamEnd:
                return []
            
            return [type().unpack(payload)] + self.ReadStream(type)
    
    def Read(self, message_type: int, payload: bytes):

        if message_type == MESSAGE_TYPES.Response:
            request = Response().unpack(payload)
        elif message_type == MESSAGE_TYPES.Empty:
            request = Empty().unpack(payload)
        elif message_type == MESSAGE_TYPES.ChatMessage:
            request = [ChatMessage().unpack(payload)]
            request = request + self.ReadStream(ChatMessage)
        elif message_type == MESSAGE_TYPES.User:
            request = User().unpack(payload)
        elif message_type == MESSAGE_TYPES.RegisterRequest:
            request = RegisterRequest().unpack(payload)
        elif message_type == MESSAGE_TYPES.LoginRequest:
            request = LoginRequest().unpack(payload)

        return request
