import grpc
from concurrent import futures
import backend.chat_service_pb2 as chat_service_pb2
import backend.chat_service_pb2_grpc as chat_service_pb2_grpc
from collections import defaultdict
import pickle
import socket


HOST = socket.gethostbyname(socket.gethostname())
PORT = '50051'
MAX_CLIENTS = 10

def storeData(db):
    """
    It opens db.pkl file in write binary mode, and then dumps our db to the file.
    """
    with open('./backend/db.pkl', 'wb') as dbfile:
        pickle.dump(db, dbfile)

def loadData():
    """
    Load the dictionary from the db.pkl file if it exists, otherwise create it.

    Return a dictionary with two keys, "passwords" and "messages".
    """
    try:
        with open('./backend/db.pkl', 'rb')  as dbfile:
            db = pickle.load(dbfile)
    except:
        db = {
            "passwords" : dict(),
            "messages": defaultdict(list)
        }
    return db

db = loadData()

class AuthServiceServicer(chat_service_pb2_grpc.AuthServiceServicer):
    """
    Define a gRPC service implementation class that inherits Auth service stub definition.

    Implements Login(), Register(), and Delete() functions
    """

    def Login(self, request, context):
        """
        Checks if a user can login based on request's credentials.
         
        Returns a success or error response.
        """
        # Get the username and password from the request message
        username = request.username 
        password = request.password 

        # Check whether the username and password match a registered user in the database
        if username in db["passwords"] and password == db["passwords"][username]:
            
            # Send response success
            response = chat_service_pb2.LoginResponse(success=True, message='Login successful')
        else:
            # Send response error if incorrect credentials are provided
            response = chat_service_pb2.LoginResponse(success=False, message='Invalid username or password')

        return response
    
    def Register(self, request, context):
        """
        Registers a user into our database.
         
        Returns a success or error response.
        """

        # Get the username and password from the request message
        username = request.username
        password = request.password

        # Check whether the username is already taken in the database
        if username not in db["passwords"]:

            # Add the username and password to the database and save the db
            db["passwords"][username] = password
            storeData(db)

            # Send response success
            response = chat_service_pb2.RegisterResponse(success=True, message='Register successful')
        else:
            # Send error response to prevent multiple users registering
            response = chat_service_pb2.RegisterResponse(success=False, message='This username is taken')

        return response
    
    def Delete(self, request, context):
        """
        Deletes a user from our database
        """
        username = request.username

        # Check if the requested user to delete is in our database
        if username in db["passwords"]:

            # Delete the account, and the messages associated with it. 
            del db["passwords"][username]
            del db["messages"][username]

            storeData(db) # Save the db

            # Send deletion response success
            response = chat_service_pb2.DeleteResponse(success=True, message='Account deleted')
        else:
            # Send deletion response error
            response = chat_service_pb2.DeleteResponse(success=False, message='Account does not exist')

        return response

class ChatServiceServicer(chat_service_pb2_grpc.ChatServiceServicer):
    """
    Define a gRPC service implementation class that inherits our chat service stub definition.

    Implements SendMessage() and ReceiveMessage() and GetUser() functions.
    """

    def SendMessage(self, request, context):
        """
        Sends a message from a sender to a recipient based on request details. 
        """
        sender = request.sender
        recipient = request.recipient
        content = request.content

        # Return error code for invalid recipient/senders
        if sender not in db["passwords"] or recipient not in db["passwords"]:
            return chat_service_pb2.SendResponse(success = False, message = "Invalid sender or recipient")

        # Store message in db and return success code
        print(f"Received message from {sender} to {recipient}: {content}")
        db["messages"][recipient].append(request)
        
        return chat_service_pb2.SendResponse(success = True, message = "Message sent")

    def GetUsers(self, request, context):
        """
        Return the current users in the database.
        """
        for user in db["passwords"]:
            yield chat_service_pb2.User(username = user)
    
    def ReceiveMessage(self, request, context):
        """
        Retrives all messages made to a recipient. Deletes 
        """
        recipient = request.username 

        # Retrieve all messages made to a recipient, deleting as we go. 
        # Loop in reverse order to maintain order messages were received.
        for i in range(len(db["messages"][recipient]) - 1, -1, -1): 
            message = db["messages"][recipient][i]
            yield chat_service_pb2.ChatMessage(sender = message.sender, content = message.content)
            db["messages"][recipient].pop()
            storeData(db)
        
def serve():
    """
    Starts the gRPC server with both Chat and Auth servicers, with a cap
    for the amount of clients it can hold, at a PORT. 
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_CLIENTS))
    chat_service_pb2_grpc.add_AuthServiceServicer_to_server(AuthServiceServicer(), server)
    chat_service_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port(HOST + ':' + PORT)
    server.start()
    print("Server initialized at " + HOST)
    server.wait_for_termination()

if __name__ == '__main__':
    serve()