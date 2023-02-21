import struct
import copy

'''
The following code defines a message protocol for a chat application. 
It defines the different types of messages that can be sent between clients and servers, 
and how to pack and unpack them into bytes.
'''

# Define the version number and header format for the message protocol
VERSION = 2
HEADER_FORMAT = "!iii"

# Define the different types of messages that can be sent
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
    Error = 10
    GetMessagesRequest = 11
    SingleMessageResponse = 12
    DeleteUserResponse = 13

# Define a base Message class that other message types will inherit from
class Message:
    def __init__(self):
        self.FORMAT = ""
        self.TYPE = -1

    # Define methods to pack and unpack the message into bytes
    def pack(self) -> bytes:
        return bytes

    def unpack(self, binary):
        return copy.deepcopy(self)

# Define a SendMessageRequest message type
class SendMessageRequest(Message):
    def __init__(self, sender = None, recipient = None, content = None):
        self.FORMAT = "!20s20s256s"
        self.TYPE = MESSAGE_TYPES.SendMessageRequest
        self.sender = sender
        self.recipient = recipient
        self.content = content

    # Implement packing and unpacking for the SendMessageRequest message type
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

# Define a Response message type
class Response(Message):
    def __init__(self, success = None, message = None):
        self.FORMAT = "!?128s"
        self.TYPE = MESSAGE_TYPES.Response
        self.success = success
        self.message = message

    # Implement packing and unpacking for the Response message type
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

# Define a GetUsersRequest message type
class GetUsersRequest(Message):
    def __init__(self, username = None):
        self.FORMAT = "!20s"
        self.TYPE = MESSAGE_TYPES.GetUsersRequest
        self.username = username

    # Implement packing and unpacking for the GetUsersRequest message type
    def pack(self) -> bytes:
        b_username = self.username.encode("ascii")
        payload = struct.pack(self.FORMAT, b_username)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary) -> Message:
        b_username = struct.unpack(self.FORMAT, binary)[0]
        self.username = b_username.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)

# Define a UsersStreamResponse message type
class UsersStreamResponse(Message):
    def __init__(self, username = None):
        self.FORMAT = "!20s"
        self.TYPE = MESSAGE_TYPES.UsersStreamResponse
        self.username = username

    # Implement packing and unpacking for the UsersStreamResponse message type
    def pack(self) -> bytes:
        b_username = self.username.encode("ascii")
        payload = struct.pack(self.FORMAT, b_username)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary):
        b_username = struct.unpack(self.FORMAT, binary)[0]
        self.username = b_username.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)

# Define a MessagesStreamResponse message type
class MessagesStreamResponse(Message):
    def __init__(self, sender = None, content = None):
        self.FORMAT = "!20s256s"
        self.TYPE = MESSAGE_TYPES.MessagesStreamResponse
        self.sender = sender
        self.content = content

    # Implement packing and unpacking for the MessagesStreamResponse message type
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

# Define a LoginRequest message type
class LoginRequest(Message):
    def __init__(self, username = None, password = None):
        self.FORMAT = "!20s20s"
        self.TYPE = MESSAGE_TYPES.LoginRequest
        self.username = username
        self.password = password

    # Implement packing and unpacking for the LoginRequest message type
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

# Define a RegisterRequest message type
class RegisterRequest(Message):
    def __init__(self, username = None, password = None):
        self.FORMAT = "!20s20s"
        self.TYPE = MESSAGE_TYPES.RegisterRequest
        self.username = username
        self.password = password

    # Implement packing and unpacking for the RegisterRequest message type
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

# Define a DeleteUserRequest message type
class DeleteUserRequest(Message):
    def __init__(self, username = None):
        self.FORMAT = "!20s"
        self.TYPE = MESSAGE_TYPES.DeleteUserRequest
        self.username = username

    # Implement packing and unpacking for the DeleteUserRequest message type
    def pack(self) -> bytes:
        b_username = self.username.encode("ascii")
        payload = struct.pack(self.FORMAT, b_username)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary):
        b_username = struct.unpack(self.FORMAT, binary)[0]
        self.username = b_username.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)

# Define a StreamEnd message type
class StreamEnd(Message):
    def __init__(self):
        self.FORMAT = "!i"
        self.TYPE = MESSAGE_TYPES.StreamEnd
    
    # Implement packing and unpacking for the StreamEnd message type
    def pack(self) -> bytes:
        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, 0)
        return header
    
    def unpack(self, binary):
        # No need to unpack, no data is being sent
        return []

# Define a Error message type
class Error(Message):
    def __init__(self, message = None):
        self.FORMAT = "!64s"
        self.TYPE = MESSAGE_TYPES.Error
        self.message = message
    
    # Implement packing and unpacking for the Error message type
    def pack(self) -> bytes:
        b_message = self.message.encode("ascii")
        payload = struct.pack(self.FORMAT, b_message)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload
    
    def unpack(self, binary):
        b_message = struct.unpack(self.FORMAT, binary)[0]
        self.message = b_message.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)

# Define a GetMessagesRequest message type
class GetMessagesRequest(Message):
    def __init__(self, username = None):
        self.FORMAT = "!20s"
        self.TYPE = MESSAGE_TYPES.GetMessagesRequest
        self.username = username

    # Implement packing and unpacking for the GetMessagesRequest message type
    def pack(self) -> bytes:
        b_username = self.username.encode("ascii")
        payload = struct.pack(self.FORMAT, b_username)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary):
        b_username = struct.unpack(self.FORMAT, binary)[0]
        self.username = b_username.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)

# Define a SingleMessageResponse message type
class SingleMessageResponse(Message):
    def __init__(self, sender = None, content = None):
        self.FORMAT = "!20s256s"
        self.TYPE = MESSAGE_TYPES.SingleMessageResponse
        self.sender = sender
        self.content = content

    # Implement packing and unpacking for the SingleMessageResponse message type 
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

# Define a DeleteUserResponse message type
class DeleteUserResponse(Message):
    def __init__(self, username = None):
        self.FORMAT = "!20s"
        self.TYPE = MESSAGE_TYPES.DeleteUserResponse
        self.username = username

    # Implement packing and unpacking for the DeleteUserResponse message type
    def pack(self) -> bytes:
        b_username = self.username.encode("ascii")
        payload = struct.pack(self.FORMAT, b_username)

        header = struct.pack(HEADER_FORMAT, VERSION, self.TYPE, len(payload))
        return header + payload

    def unpack(self, binary):
        b_username = struct.unpack(self.FORMAT, binary)[0]
        self.username = b_username.decode("ascii").rstrip('\x00')
        return copy.deepcopy(self)