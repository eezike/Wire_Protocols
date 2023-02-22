import grpc
from concurrent import futures
import backend.chat_service_pb2 as chat_service_pb2 
import backend.chat_service_pb2_grpc as chat_service_pb2_grpc
import backend.client
from backend.database import Database
import os
from os.path import exists
import time
import threading
import pickle

# reset the database before importing the server (before server instantiates database)
def reset_database():
    db_filename = './backend/db.pkl'
    if exists(db_filename):
        os.remove(db_filename)
        print('Old database removed')

reset_database()

from server import Server, AuthServiceServicer, ChatServiceServicer

HOST = 'localhost'
PORT = '50051'

# Run the server
def serve():
    MAX_CLIENTS = 10
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_CLIENTS))
    chat_service_pb2_grpc.add_AuthServiceServicer_to_server(AuthServiceServicer(), server)
    chat_service_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port(HOST + ':' + PORT)
    server.start()
    print("Server initialized at " + HOST + ', ' PORT)
    server.wait_for_termination()

def connect():
    channel = grpc.insecure_channel(HOST + ':' + str(PORT)) 
    auth_stub = chat_service_pb2_grpc.AuthServiceStub(channel)
    chat_stub = chat_service_pb2_grpc.ChatServiceStub(channel)
    return auth_stub, chat_stub

class UnitTester:

    def __init__(self, auth_stub, chat_stub) -> None:
        self.auth_stub = auth_stub
        self.chat_stub = chat_stub

        # For authentication tests
        self.username1 = "testing1"
        self.username2 = "testing2"
        self.password = "12345"
    
    """
    Testing authentication services.
    """
    def test_login(self, username, password):
        # Ensure auth stub responds with success for login
        request = chat_service_pb2.LoginRequest(username=username, password=password)
        response = self.auth_stub.Login(request)
        assert response.success, "Test login: auth stub error"

    def test_login_errors(self):
        # Case 1: user does not exist in db
        request = chat_service_pb2.LoginRequest(username="fail", password=self.password)
        response = self.auth_stub.Login(request)
        assert not response.success, "Test login error: auth stub was successful, expected error in user"

        # Case 2: user exists wrong password
        request = chat_service_pb2.LoginRequest(username=self.username1, password="fail")
        response = self.auth_stub.Login(request)
        assert not response.success, "Test login error: auth stub was successful, expected error in password"

    def test_register(self, username, password):
        # Ensure stub responds with success for register
        request = chat_service_pb2.RegisterRequest(username=username, password=password)
        response = self.auth_stub.Register(request)
        assert response.success, "Test register: auth stub error"

        # Double check database to see if user was saved
        try:
            with open('./backend/db.pkl', 'rb')  as dbfile:
                db = pickle.load(dbfile)
            assert username in db["passwords"], "Test register: created user not in db"
        except:
            assert False, "Test register: db file does not exist"

    def test_register_errors(self):
        # Check user1 already in db
        request = chat_service_pb2.RegisterRequest(username=self.username1, password=self.password)
        response = self.auth_stub.Register(request)
        assert not response.success, "Test register error: expected error as user1 already in db"

        # Check user2 already in db
        request = chat_service_pb2.RegisterRequest(username=self.username2, password=self.password)
        response = self.auth_stub.Register(request)
        assert not response.success, "Test register error: expected error as user1 already in db"

    def test_delete(self, username):
        # Ensure stub responds with success for deletion
        request = chat_service_pb2.DeleteRequest(username = username)
        response = self.auth_stub.Delete(request)
        assert response.success, "Test delete: auth stub error"

        # Double check database to see if user was deleted
        try:
            with open('./backend/db.pkl', 'rb')  as dbfile:
                db = pickle.load(dbfile)
            assert username not in db["passwords"], "Test deletion: created user still in db"
        except:
            assert False, "Test delete: db file does not exist"
        
    """
    Testing chat services
    """
    def test_messages(self):
        pass

    def test_messages_error(self):
        pass
    
    def test_get_users(self):
        # Get a list of usernamers from the chat_stub
        userObjs = self.chat_stub.GetUsers(chat_service_pb2.Empty()) 
        users = [userObj.username for userObj in userObjs]
        assert sorted(users) == sorted([self.username1, self.username2]), "Test get users: non-matching user lists"

    # client/server integration with protobufs
    def test_client(self):
        pass

    def test_server(self):
        pass
        
    def run_tests(self):
        self.test_register(self.username1, self.password)
        self.test_register(self.username2, self.password)
        self.test_register_errors()
        self.test_login(self.username1, self.password)
        self.test_login(self.username2, self.password)
        self.test_login_errors()
        self.test_delete()
        self.test_messages()
        self.test_get_users()
        self.test_delete()
        self.test_delete()
        self.test_client()
        self.test_server()

if __name__ == '__main__':
    threading.Thread(target = serve).start()
    auth_stub, chat_stub = connect()
    tester = UnitTester(auth_stub, chat_stub)
    tester.run_tests()