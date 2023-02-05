import struct
from enum import Enum 

VERSION = 1

# Define the header format for the wire protocol
HEADER_FORMAT = "!iii"

# Define the message types
class MSG_TYPES(Enum):
    LOGIN = 1
    REGISTER = 2
    SEND_MSG = 3
    GET_MSG = 4
    RESPONSE = 5


# Define the message types
class MSG_FORMAT(Enum):
    LOGIN = "!20s20s"
    REGISTER = "!20s20s"
    SEND_MSG = "!20s20s256s"
    GET_MSG = "!i"
    RESPONSE = "!i"

def encode_message(msg_type, **kwargs):
    # Could use switch cases for clarity, but introduced in python 3.10
    if msg_type == MSG_TYPES.LOGIN:
        request = struct.pack(MSG_FORMAT.LOGIN, kwargs.username.encode(), kwargs.password.encode())
        payload = pack_message(request)
    elif msg_type == MSG_TYPES.REGISTER:
        payload = struct.pack(MSG_FORMAT.REGISTER, kwargs.username.encode(), kwargs.password.encode())
    elif msg_type == MSG_TYPES.SEND_MSG:
        pass
    elif msg_type == MSG_TYPES.GET_MSG:
        pass
    elif msg_type == MSG_TYPES.RESPONSE:
        pass
    else:
        print("Error: invalid message type")
        return None
    
    return pack_message(msg_type, pack_message(request))

# Define the maximum size for the payload
MAX_PAYLOAD_SIZE = 1024

def pack_message(message_type, payload):
    """Pack the message into a binary format"""
    header = struct.pack(HEADER_FORMAT, VERSION, message_type, len(payload))
    return header + payload

def unpack_message(message_type, smessage):
    """Unpack the binary message into the original format"""
    header = message[:struct.calcsize(HEADER_FORMAT)]
    message_type, payload_size = struct.unpack(HEADER_FORMAT, header)
    payload = message[struct.calcsize(HEADER_FORMAT):struct.calcsize(HEADER_FORMAT) + payload_size]
    return message_type, payload



def receive_message(socket):
    """Receive a message from the socket"""
    header = socket.recv(struct.calcsize(HEADER_FORMAT))
    _, message_type, payload_size = struct.unpack(HEADER_FORMAT, header)
    payload = socket.recv(payload_size)
    return message_type, payload

def send_message(socket, message_type, payload):
    """Send a message over the socket"""
    message = pack_message(message_type, payload)
    socket.sendall(message)


# # Pack header, login request into a single message
# def pack_login_request(username, password):
#     login_request = struct.pack(LOGIN_REQUEST_FORMAT, username.encode(), password.encode())
#     return pack_message(1, login_request)

# # Unpack header, login request from a single message
# def unpack_login_request(message):
#     message_id, login_request = unpack_message(message)
#     username, password = struct.unpack(LOGIN_REQUEST_FORMAT, login_request)
#     return username.decode(), password.decode()

# # Pack header, login response into a single message
# def pack_login_response(status):
#     login_response = struct.pack(LOGIN_RESPONSE_FORMAT, status)
#     return pack_message(2, login_response)

# # Unpack header, login response from a single message
# def unpack_login_response(message):
#     message_id, login_response = unpack_message(message)
#     status, = struct.unpack(LOGIN_RESPONSE_FORMAT, login_response)
#     return status

# # Example usage
# message = pack_login_request("john", "doe")
# username, password = unpack_login_request(message)
# print(username, password)
# # Output: john doe

# message = pack_login_response(0)
# status = unpack_login_response(message)
# print(status)
# # Output: 0
