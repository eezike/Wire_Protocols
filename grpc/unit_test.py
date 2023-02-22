import unittest
import grpc
import pickle
from server import Server, AuthServiceServicer, ChatServiceServicer
import backend.client
import backend.chat_service_pb2
import backend.chat_service_pb2_grpc

class UnitTester(unittest.TestCase):
    
    """
    Testing authentication services.
    """
    def test_login():
        pass

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
    unittest.main()