import grpc
from concurrent import futures
import time
import chat_service_pb2
import chat_service_pb2_grpc

class ChatService(chat_service_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.messages = []
        self.active_streams = {}

    def SendMessage(self, request, context):
        print(f"Received message from {request.sender_username} to {request.recipient_username}: {request.content}")
        self.messages.append(request)
        if request.recipient_username in self.active_streams:
            self.active_streams[request.recipient_username].send_message(request)
        return chat_service_pb2.Empty()

    def JoinChat(self, request, context):
        username = request.username
        stream = context.otherside_context().wrap(grpc.server_streaming).invoke_rpc()
        self.active_streams[username] = stream
        for message in self.messages:
            if message.recipient_username == username:
                stream.send_message(message)
        return chat_service_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_service_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
