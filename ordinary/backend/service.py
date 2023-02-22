import struct
import socket
from backend.service_classes import VERSION, HEADER_FORMAT, MESSAGE_TYPES, Message, SendMessageRequest, Response, GetUsersRequest, UsersStreamResponse, MessagesStreamResponse, LoginRequest, RegisterRequest, DeleteUserRequest, StreamEnd, Error, GetMessagesRequest, SingleMessageResponse, DeleteUserResponse, AddUserResponse

class Stub:
    '''
    Class for sending, receiving, and parsing the defined message types
    '''
    def __init__(self, socket: socket, client : bool = False):
        # Initialize the socket and client instance variables
        self.socket = socket
        self.client = client
        
        # Define a dictionary that maps message types to message classes
        self.single_message_types_to_class = {
            MESSAGE_TYPES.SendMessageRequest :  SendMessageRequest,
            MESSAGE_TYPES.Response :  Response,
            MESSAGE_TYPES.GetUsersRequest :  GetUsersRequest,
            MESSAGE_TYPES.LoginRequest :  LoginRequest,
            MESSAGE_TYPES.RegisterRequest :  RegisterRequest,
            MESSAGE_TYPES.DeleteUserRequest :  DeleteUserRequest,
            MESSAGE_TYPES.StreamEnd :  StreamEnd,
            MESSAGE_TYPES.Error : Error,
            MESSAGE_TYPES.GetMessagesRequest: GetMessagesRequest,
            MESSAGE_TYPES.SingleMessageResponse: SingleMessageResponse,
            MESSAGE_TYPES.DeleteUserResponse: DeleteUserResponse,
            MESSAGE_TYPES.AddUserResponse: AddUserResponse
        }

        # Define another dictionary that maps stream message types to message classes
        self.stream_message_types_to_class = {
            MESSAGE_TYPES.UsersStreamResponse :  UsersStreamResponse,
            MESSAGE_TYPES.MessagesStreamResponse :  MessagesStreamResponse
        }

    # Define a method to send a message to the socket
    def Send(self, payload: Message, recieve = True) -> Message:
        # Convert the payload message to binary format
        binary_payload = payload.pack()
        # Send the binary payload to the socket
        self.socket.sendall(binary_payload)

        # If client or receive is true, receive the message and return the response
        if self.client and recieve:
            message_type, payload = self.Recv()
            return self.Parse(message_type, payload)
    
    # Define a method to send a message stream to the socket
    def SendStream(self, payload_iterator: list[Message], recieve = False) -> Message:
        binary_payload = bytes()
        # Convert each message in the payload iterator to binary format and concatenate them
        for req in payload_iterator:
            binary_payload += req.pack()
        # Append the end of the message stream tag to the end of the concatenated binary payload
        binary_payload += StreamEnd().pack()

        # Send the binary payload to the socket
        self.socket.sendall(binary_payload)
    
    # Define a method to receive a message from the socket
    def Recv(self) -> tuple[int, bytes]:
        """Receive a message from the socket"""
        # Receive the header of the message from the socket
        header = self.socket.recv(struct.calcsize(HEADER_FORMAT))

        # If the header is empty, raise a ConnectionResetError
        if not header:
            print("Connection broken by client")
            raise ConnectionResetError

        # Unpack the header data to get the message version, type, and payload size
        version, message_type, payload_size = struct.unpack(HEADER_FORMAT, header)

        # If the version is incorrect, rais an exception
        if version != VERSION:
            raise Exception("Error: incorrect version #" + str(version))
        
        # Receive the payload of the message from the socket
        payload = self.socket.recv(payload_size)

        # Return the message type and payload as a tuple
        return message_type, payload
    
    def ParseStream(self, expected_message_type: int) -> list[Message]:
        # Get the expected message type class
        class_type : Message = self.stream_message_types_to_class[expected_message_type]
        
        # Loop up to 100 times to receive messages from the socket
        for _ in range(100):
            # Receive a message from the socket
            message_type, payload = self.Recv()

            # Check if the message is a stream end
            if message_type == MESSAGE_TYPES.StreamEnd:
                return []
            
            # Check if the received message type matches the expected message type
            if message_type != expected_message_type:
                raise Exception(f"Unexpected message type {message_type} caught in stream for message type {expected_message_type}")
            
            # Parse the payload and add it to the result list
            return [class_type().unpack(payload)] + self.ParseStream(expected_message_type)

    def Parse(self, message_type: int, payload: bytes) -> Message:

        # Check if the message type is a single message type or a stream message type
        if message_type in self.single_message_types_to_class:
            # Parse the payload as a single message
            res = self.single_message_types_to_class[message_type]().unpack(payload)
        elif message_type in self.stream_message_types_to_class:
            # Parse the payload as a stream message
            class_type : Message = self.stream_message_types_to_class[message_type]
            res = [class_type().unpack(payload)]
            res = res + self.ParseStream(message_type)
        else:
            # If the message type is unknown, return a Error with a message indicating that the message type is unknown
            res = Error(message= "Unknown message type")

        return res