import struct


VERSION = 2
HEADER_FORMAT = "!iii"

class MESSAGE_TYPES():
    SendRequest = 1
    Response = 2
    Empty = 3
    ChatMessage = 4
    User = 5
    LoginRequest = 6
    RegisterRequest = 7
    StreamEnd = 8

class Message:
    def __init__(self):
        self.FORMAT = ""
        self.TYPE = -1
    
    def pack(self) -> bytes:
        return bytes
    
    def unpack(self, binary):
        pass


class SendRequest(Message):
    def __init__(self, sender = None, recipient = None, content = None):
        self.FORMAT = "!20s20s256s"
        self.TYPE = MESSAGE_TYPES.SendRequest
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


class Empty(Message):
    def __init__(self):
        self.FORMAT = ""
        self.TYPE = MESSAGE_TYPES
        pass
    
    def pack(self) -> bytes:
        pass
    
    def unpack(self, binary):
        pass

class ChatMessage(Message):
    def __init__(self, sender = None, content = None):
        self.FORMAT = "!20s256s"
        self.TYPE = MESSAGE_TYPES
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

class User(Message):
    def __init__(self, username = None):
        self.FORMAT = "!20s"
        self.TYPE = MESSAGE_TYPES
        self.username = username

    def pack(self) -> bytes:
        b_username = self.username.encode("ascii")
        payload = struct.pack(self.FORMAT, b_username)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary):
        pass


class LoginRequest(Message):
    def __init__(self, username = None, password = None):
        self.FORMAT = "!20s20s"
        self.TYPE = MESSAGE_TYPES
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
        self.TYPE = MESSAGE_TYPES
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


class StreamEnd(Message):
    def __init__(self):
        self.FORMAT = "!i"
        self.TYPE = MESSAGE_TYPES.StreamEnd
        pass
    
    def pack(self) -> bytes:
        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, 0)
        return header
    
    def unpack(self, binary):
        pass