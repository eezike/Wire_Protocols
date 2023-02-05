import struct

VERSION = 1

# Define the header format for the wire protocol
HEADER_FORMAT = "!iii"

# Define the message types
class MSG_TYPES():
    LOGIN = 1
    REGISTER = 2
    SEND_MSG = 3
    GET_MSG = 4
    RESPONSE = 5

# Define the message types
class MSG_FORMAT():
    LOGIN = "!20s20s"
    REGISTER = "!20s20s"
    SEND_MSG = "!20s20s256s"
    GET_MSG = "!i"
    RESPONSE = "!i"

# Define these response code types
class RESPONSE_CODE():
    LOGIN_SUCCESS = 1
    LOGIN_INVALID_PASSWORD = 2
    REGISTER_SUCCESS = 3
    REGISTER_INVALID_USERNAME = 4
    AUTH_ERROR = 5
    

# Define the maximum size for the payload
MAX_PAYLOAD_SIZE = 1024

def pack_message(message_type, **kwargs):
    print(kwargs)
    # Could use switch cases for clarity, but introduced in python 3.10
    if message_type == MSG_TYPES.LOGIN:
        b_username = kwargs.get("username", None).encode("ascii")
        b_password = kwargs.get("password", None).encode("ascii")
        payload = struct.pack(MSG_FORMAT.LOGIN, b_username, b_password)
    elif message_type == MSG_TYPES.REGISTER:
        b_username = kwargs.get("username", None).encode("ascii")
        b_password = kwargs.get("password", None).encode("ascii")
        payload = struct.pack(MSG_FORMAT.REGISTER, b_username, b_password)
    elif message_type == MSG_TYPES.SEND_MSG:
        pass
    elif message_type == MSG_TYPES.GET_MSG:
        pass
    elif message_type == MSG_TYPES.RESPONSE:
        payload = struct.pack(MSG_FORMAT.RESPONSE, kwargs.get("response_code", None))
    else:
        print("Error: invalid message type")
        return None
    
    header = struct.pack(HEADER_FORMAT, VERSION, message_type, len(payload))
    return header + payload


def send_message(socket, binary_message):
    """Send a message over the socket"""
    socket.sendall(binary_message)

def send(socket, message_type, **kwargs):
    """
    Sends a message to client/server via socket.

    Parameters
    ----------
    socket : 
        socket that you want to send the message to
    message_type : MSG_TYPES
        declare the type of message in order to be decoded properly
    **kwargs : dict()

    """
    message = pack_message(message_type, **kwargs)
    send_message(socket, message)








def receive_message(socket):
    """Receive a message from the socket"""
    header = socket.recv(struct.calcsize(HEADER_FORMAT))
    version, message_type, payload_size = struct.unpack(HEADER_FORMAT, header)
    if version != VERSION:
        print("Error: incorrect version")
        return
    payload = socket.recv(payload_size)
    return message_type, payload

def unpack_payload(message_type, payload):
    """Unpack the binary message into the original format"""

    if message_type == MSG_TYPES.LOGIN:
        b_username, b_password = struct.unpack(MSG_FORMAT.LOGIN, payload)
        return b_username.decode("ascii").rstrip('\x00'), b_password.decode("ascii").rstrip('\x00')
    elif message_type == MSG_TYPES.REGISTER:
        FORMAT = MSG_FORMAT.REGISTER
    elif message_type == MSG_TYPES.SEND_MSG:
        pass
    elif message_type == MSG_TYPES.GET_MSG:
        pass
    elif message_type == MSG_TYPES.RESPONSE:
        response_code = struct.unpack(MSG_FORMAT.RESPONSE, payload)
        return response_code
    else:
        print("Error: ")
        return 