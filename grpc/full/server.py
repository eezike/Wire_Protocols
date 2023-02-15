import grpc
from concurrent import futures
import chat_service_pb2
import chat_service_pb2_grpc
import pickle


def storeData(db):
    with open('db.pkl', 'wb') as dbfile:
        pickle.dump(db, dbfile)

  
def loadData():
    try:
        with open('db.pkl', 'rb')  as dbfile:
            db = pickle.load(dbfile)
    except:
        db = {
            "passwords" : dict(),
            "active_streams": dict(),
            "messages": []
        }
    
    return db

db = loadData()


class AuthServiceServicer(chat_service_pb2_grpc.AuthServiceServicer):
    def Login(self, request, context):

        username = request.username 
        password = request.password 

        if username in db["passwords"] and password == db["passwords"][username]:

            # store newly logged in user's stream
            stream = context.otherside_context().wrap(grpc.server_streaming).invoke_rpc()
            db["active_streams"][username] = stream
            storeData(db)

            # send logged in user all their messages
            for message in db["messages"]:
                if message.recipient_username == username:
                    stream.send_message(message)
                    db["messages"].remove(message)
            
            response = chat_service_pb2.LoginResponse(success=True, message='Login successful')
        else:
            response = chat_service_pb2.LoginResponse(success=False, message='Invalid username or password')


        return response
    
    def Register(self, request, context):

        username = request.username
        password = request.password

        if username not in db["passwords"]:
            
            # add new user to active streams
            stream = context.otherside_context().wrap(grpc.server_streaming).invoke_rpc()
            db["active_streams"][username] = stream

            # register the user
            db["passwords"][username] = password
            storeData(db)

            response = chat_service_pb2.LoginResponse(success=True, message='Register successful')
        else:
            response = chat_service_pb2.LoginResponse(success=False, message='This username is taken')


        return response

class ChatServiceServicer(chat_service_pb2_grpc.ChatServiceServicer):
    def SendMessage(self, request, context):

        sender_username = request.sender_username
        recipient_username = request.recipient_username
        content = request.content

        if sender_username not in db["passwords"]:
            # send an error later
            return chat_service_pb2.Empty()

        print(f"Received message from {sender_username} to {recipient_username}: {content}")
        
        if recipient_username in db["active_streams"]:
            db["active_streams"][recipient_username].send_message(request)
        else:
            db["messages"].append(request)

        return chat_service_pb2.Empty()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_service_pb2_grpc.add_AuthServiceServicer_to_server(AuthServiceServicer(), server)
    chat_service_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()