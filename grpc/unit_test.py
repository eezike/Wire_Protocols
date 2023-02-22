import unittest
import grpc
from concurrent import futures
import pickle
from server import Server, AuthServiceServicer, ChatServiceServicer
import backend.client
import backend.chat_service_pb2 as chat_service_pb2 
import backend.chat_service_pb2_grpc as chat_service_pb2_grpc

HOST = 'localhost'
PORT = '50051'
channel = auth_stub = chat_stub = None

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

class UnitTester(unittest.TestCase):
    
    """
    Testing authentication services.
    """
    def test_login():
        

    def test_register():
        pass

    def test_delete():
        pass

    """
    Testing chat services
    """
    def test_messages():
        pass
    
    def test_get_users():
        pass

    # client/server integration with protobufs
    def test_client():
        pass

    def test_server():
        pass
        

if __name__ == '__main__':
    serve()
    connect()
    unittest.main()