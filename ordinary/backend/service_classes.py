import struct
import copy


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
        return copy.deepcopy(self)


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

    def unpack(self, binary) -> Message:
        b_sender, b_recipient, b_content = struct.unpack(self.FORMAT, binary)
        self.sender = b_sender.decode("ascii").rstrip('\x00')
        self.recipient = b_recipient.decode("ascii").rstrip('\x00')
        self.content = b_content.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)


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

    def unpack(self, binary) -> Message:
        b_success, b_message = struct.unpack(self.FORMAT, binary)
        self.success = b_success
        self.message = b_message.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)

    def __repr__(self) -> str:
        return f"Success: {self.success}; Message: {self.message}"

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

    def unpack(self, binary) -> Message:
        b_username = struct.unpack(self.FORMAT, binary)[0]
        self.username = b_username.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)

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
        b_username = struct.unpack(self.FORMAT, binary)[0]
        self.username = b_username.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)

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
        b_sender, b_content = struct.unpack(self.FORMAT, binary)
        self.sender = b_sender.decode("ascii").rstrip('\x00')
        self.content = b_content.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)

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
        b_username, b_password = struct.unpack(self.FORMAT, binary)
        self.username = b_username.decode("ascii").rstrip('\x00')
        self.password = b_password.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)


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
        b_username, b_password = struct.unpack(self.FORMAT, binary)
        self.username = b_username.decode("ascii").rstrip('\x00')
        self.password = b_password.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)

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
        b_username = struct.unpack(self.FORMAT, binary)[0]
        self.username = b_username.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)


class StreamEnd(Message):
    def __init__(self):
        self.FORMAT = "!i"
        self.TYPE = MESSAGE_TYPES.StreamEnd
    
    def pack(self) -> bytes:
        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, 0)
        return header
    
    def unpack(self, binary):
        # _ = struct.unpack(self.FORMAT, binary)
        return []

class Empty(Message):
    def __init__(self):
        self.FORMAT = ""
        self.TYPE = MESSAGE_TYPES.Empty
    
    def pack(self) -> bytes:
        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, 0)
        return header
    
    def unpack(self, binary):
        _ = struct.unpack(self.FORMAT, binary)
        return copy.deepcopy(self)

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
        b_username = struct.unpack(self.FORMAT, binary)[0]
        self.username = b_username.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)

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
        b_sender, b_content = struct.unpack(self.FORMAT, binary)
        self.sender = b_sender.decode("ascii").rstrip('\x00')
        self.content = b_content.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)