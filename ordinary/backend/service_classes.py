import struct


VERSION = 2
HEADER_FORMAT = "!iii"

class MESSAGE_TYPES():
    SendMessageRequest = 1
    Response = 2
    GetUsersRequest = 3
    UsersStreamResponse = 4
    MessagesStreamResponse = 5
    LoginRequest = 6
    RegisterRequest = 7
    DeleteUserRequest = 8
    StreamEnd = 9
    Empty = 10
    GetMessagesRequest = 11
    SingleMessageResponse = 12




class Message:
    def __init__(self):
        self.FORMAT = ""
        self.TYPE = -1
    
    def pack(self) -> bytes:
        return bytes
    
    def unpack(self, binary):
        pass


class SendMessageRequest(Message):
    def __init__(self, sender = None, recipient = None, content = None):
        self.FORMAT = "!20s20s256s"
        self.TYPE = MESSAGE_TYPES.SendMessageRequest
        self.sender = sender
        self.recipient = recipient
        self.content = content

    def pack(self) -> bytes:
        b_sender = self.sender.encode("ascii")
        b_recipient = self.recipient.encode("ascii")
        b_content = self.content.encode("ascii")
        payload = struct.pack(self.FORMAT, b_sender, b_recipient, b_content)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary):
        pass


class Response(Message):
    def __init__(self, success = None, message = None):
        self.FORMAT = "!?128s"
        self.TYPE = MESSAGE_TYPES.Response
        self.success = success
        self.message = message

    def pack(self) -> bytes:
        b_success = self.success
        b_message = self.message.encode("ascii")
        payload = struct.pack(self.FORMAT, b_success, b_message)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary):
        pass

class GetUsersRequest(Message):
    def __init__(self, username = None):
        self.FORMAT = "!20s"
        self.TYPE = MESSAGE_TYPES.GetUsersRequest
        self.username = username

    def pack(self) -> bytes:
        b_username = self.username.encode("ascii")
        payload = struct.pack(self.FORMAT, b_username)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary):
        pass

class UsersStreamResponse(Message):
    def __init__(self, username = None):
        self.FORMAT = "!20s"
        self.TYPE = MESSAGE_TYPES.UsersStreamResponse
        self.username = username

    def pack(self) -> bytes:
        b_username = self.username.encode("ascii")
        payload = struct.pack(self.FORMAT, b_username)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary):
        pass

class MessagesStreamResponse(Message):
    def __init__(self, sender = None, content = None):
        self.FORMAT = "!20s256s"
        self.TYPE = MESSAGE_TYPES.MessagesStreamResponse
        self.sender = sender
        self.content = content

    def pack(self) -> bytes:
        b_sender = self.sender.encode("ascii")
        b_content = self.content.encode("ascii")
        payload = struct.pack(self.FORMAT, b_sender, b_content)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary):
        pass

class LoginRequest(Message):
    def __init__(self, username = None, password = None):
        self.FORMAT = "!20s20s"
        self.TYPE = MESSAGE_TYPES.LoginRequest
        self.username = username
        self.password = password

    def pack(self) -> bytes:
        b_username = self.username.encode("ascii")
        b_password = self.password.encode("ascii")
        payload = struct.pack(self.FORMAT, b_username, b_password)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary):
        pass


class RegisterRequest(Message):
    def __init__(self, username = None, password = None):
        self.FORMAT = "!20s20s"
        self.TYPE = MESSAGE_TYPES.RegisterRequest
        self.username = username
        self.password = password

    def pack(self) -> bytes:
        b_username = self.username.encode("ascii")
        b_password = self.password.encode("ascii")
        payload = struct.pack(self.FORMAT, b_username, b_password)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary):
        pass

class DeleteUserRequest(Message):
    def __init__(self, username = None):
        self.FORMAT = "!20s"
        self.TYPE = MESSAGE_TYPES.DeleteUserRequest
        self.username = username

    def pack(self) -> bytes:
        b_username = self.username.encode("ascii")
        payload = struct.pack(self.FORMAT, b_username)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary):
        pass


class StreamEnd(Message):
    def __init__(self):
        self.FORMAT = "!i"
        self.TYPE = MESSAGE_TYPES.StreamEnd
    
    def pack(self) -> bytes:
        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, 0)
        return header
    
    def unpack(self, binary):
        pass

class Empty(Message):
    def __init__(self):
        self.FORMAT = ""
        self.TYPE = MESSAGE_TYPES.Empty
    
    def pack(self) -> bytes:
        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, 0)
        return header
    
    def unpack(self, binary):
        pass

class GetMessagesRequest(Message):
    def __init__(self, username = None):
        self.FORMAT = "!20s"
        self.TYPE = MESSAGE_TYPES.GetMessagesRequest
        self.username = username

    def pack(self) -> bytes:
        b_username = self.username.encode("ascii")
        payload = struct.pack(self.FORMAT, b_username)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary):
        pass

class SingleMessageResponse(Message):
    def __init__(self, sender = None, content = None):
        self.FORMAT = "!20s256s"
        self.TYPE = MESSAGE_TYPES.MessagesStreamResponse
        self.sender = sender
        self.content = content

    def pack(self) -> bytes:
        b_sender = self.sender.encode("ascii")
        b_content = self.content.encode("ascii")
        payload = struct.pack(self.FORMAT, b_sender, b_content)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload
    
    def unpack(self, binary):
        pass