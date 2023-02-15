import struct

VERSION = 1

# Define the header format for the wire protocol
HEADER_FORMAT = "!iii"

# Define the message types
class MSG_TYPES():
    LOGIN = 1
    REGISTER = 2
    SEND_MSG = 3
    RES_MSGS = 4
    RESPONSE = 5
    xxxxx = 6
    RES_USERS = 7

# Define the message types
class MSG_FORMAT():
    LOGIN = "!20s20s"
    REGISTER = "!20s20s"
    SEND_MSG = "!20s20s256s"
    RES_MSGS = "!i"
    RESPONSE = "!i"
    RES_USERS = "!20s"

# Define these response code types
class RESPONSE_CODE():
    LOGIN_SUCCESS = 1
    LOGIN_INVALID_PASSWORD = 2
    LOGIN_NO_ACCOUNT = 3
    REGISTER_SUCCESS = 4
    REGISTER_INVALID_USERNAME = 5
    AUTH_ERROR = 6
    WELCOME = 7
    REQ_USERS = 8
    UNKNOWN_ERROR = 404

# Define the maximum size for the payload
MAX_PAYLOAD_SIZE = 1024

def pack_message(message_type: int, **kwargs) -> bytes:
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
        b_to = kwargs.get("_to", None).encode("ascii")
        b_from = kwargs.get("_from", None).encode("ascii")
        b_msg = kwargs.get("msg", None).encode("ascii")
        payload = struct.pack(MSG_FORMAT.SEND_MSG, b_to, b_from, b_msg)
    elif message_type == MSG_TYPES.RES_MSGS:
        payload = struct.pack(MSG_FORMAT.RES_MSGS, 1)
    elif message_type == MSG_TYPES.RESPONSE:
        response_code = kwargs.get("response_code", None)
        payload = struct.pack(MSG_FORMAT.RESPONSE, response_code)
    elif message_type == MSG_TYPES.RES_USERS:
        user = kwargs.get("user", None).encode("ascii")
        payload = struct.pack(MSG_FORMAT.RES_USERS, user)
    else:
        print("Error: invalid message type")
        return None

    header = struct.pack(HEADER_FORMAT, VERSION, message_type, len(payload))
    return header + payload


def sendone(socket: any, message_type: int, **kwargs) -> None:
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
    binary_message = pack_message(message_type, **kwargs)
    return socket.sendall(binary_message)



def receive_message(socket: any) -> tuple[int, bytes]:
    """Receive a message from the socket"""
    header = socket.recv(struct.calcsize(HEADER_FORMAT))
    version, message_type, payload_size = struct.unpack(HEADER_FORMAT, header)
    if version != VERSION:
        print("Error: incorrect version #" + str(version))
        return None, None
    payload = socket.recv(payload_size)
    return message_type, payload

def unpack_payload(message_type: int, payload: bytes) -> any:
    """Unpack the binary message into the original format"""

    if message_type == MSG_TYPES.LOGIN:
        b_username, b_password = struct.unpack(MSG_FORMAT.LOGIN, payload)
        return b_username.decode("ascii").rstrip('\x00'), b_password.decode("ascii").rstrip('\x00')
    elif message_type == MSG_TYPES.REGISTER:
        b_username, b_password = struct.unpack(MSG_FORMAT.REGISTER, payload)
        return b_username.decode("ascii").rstrip('\x00'), b_password.decode("ascii").rstrip('\x00')
    elif message_type == MSG_TYPES.SEND_MSG:
        b_to, b_from, b_msg = struct.unpack(MSG_FORMAT.SEND_MSG, payload)
        return b_to.decode("ascii").rstrip('\x00'), b_from.decode("ascii").rstrip('\x00'), b_msg.decode("ascii").rstrip('\x00')
    elif message_type == MSG_TYPES.RES_MSGS:
        pass
    elif message_type == MSG_TYPES.RESPONSE:
        response_code = struct.unpack(MSG_FORMAT.RESPONSE, payload)
        return response_code[0]
    elif message_type == MSG_TYPES.RES_USERS:
        b_user = struct.unpack(MSG_FORMAT.RES_USERS, payload)[0]
        return b_user.decode("ascii").rstrip('\x00')
    else:
        print("Error: ")
        return 