import grpc
from concurrent import futures
import backend.chat_service_pb2 as chat_service_pb2 
import backend.chat_service_pb2_grpc as chat_service_pb2_grpc
from server import Server, AuthServiceServicer, ChatServiceServicer
import backend.client
from backend.database import Database
import os
from os.path import exists
import time

HOST = 'localhost'
PORT = '50051'

def serve():
    MAX_CLIENTS = 10
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_CLIENTS))
    chat_service_pb2_grpc.add_AuthServiceServicer_to_server(AuthServiceServicer(), server)
    chat_service_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port(HOST + ':' + PORT)
    server.start()
    print("Server initialized at " + HOST)
    server.wait_for_termination()

def connect():
    channel = grpc.insecure_channel(HOST + ':' + str(PORT)) 
    auth_stub = chat_service_pb2_grpc.AuthServiceStub(channel)
    chat_stub = chat_service_pb2_grpc.ChatServiceStub(channel)
    return auth_stub, chat_stub

def init_database():
    db_filename = './backend/db.pkl'
    if exists(db_filename):
        os.remove(db_filename)
        print('Old database removed')
        time.sleep(1)

    db = Database(db_filename)
    db.loadData()
    db.storeData()
    print("New database created")
    return db

class UnitTester:

    def __init__(self, auth_stub, chat_stub, db) -> None:
        self.auth_stub = auth_stub
        self.chat_stub = chat_stub
        self.db = db
    
    """
    Testing authentication services.
    """
    def test_login(self):
        pass



    def test_register(self):
        # Ensure stub responds with success
        username, password = "testing", "12345"
        request = chat_service_pb2.RegisterRequest(username=username, password=password)
        response = self.auth_stub.Register(request)
        assert response.success, "Test register: auth stub error"

        # Double check database
        assert username in db.get_db()["passwords"], "Test register: created user not in db"

    def test_delete(self):
        pass

    """
    Testing chat services
    """
    def test_messages(self):
        pass
    
    def test_get_users(self):
        pass

    # client/server integration with protobufs
    def test_client(self):
        pass

    def test_server(self):
        pass
        
    def run_tests(self):
        self.test_register()
        self.test_login()
        self.test_delete()
        self.test_messages()
        self.test_get_users()
        self.test_client()
        self.test_server()

if __name__ == '__main__':
    serve()
    auth_stub, chat_stub = connect()
    db = init_database()
    tester = UnitTester(auth_stub, chat_stub, db)
    tester.run_tests()