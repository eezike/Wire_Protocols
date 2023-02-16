import grpc
from concurrent import futures
import chat_service_pb2
import chat_service_pb2_grpc
from collections import defaultdict
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
            "messages": defaultdict(list)
        }
    
    return db

db = loadData()



class AuthServiceServicer(chat_service_pb2_grpc.AuthServiceServicer):

    def Login(self, request, context):

        username = request.username 
        password = request.password 

        if username in db["passwords"] and password == db["passwords"][username]:
            
            response = chat_service_pb2.LoginResponse(success=True, message='Login successful')
        else:
            response = chat_service_pb2.LoginResponse(success=False, message='Invalid username or password')


        return response
    
    def Register(self, request, context):

        username = request.username
        password = request.password

        if username not in db["passwords"]:

            # register the user
            db["passwords"][username] = password
            storeData(db)

            response = chat_service_pb2.RegisterResponse(success=True, message='Register successful')
        else:
            response = chat_service_pb2.RegisterResponse(success=False, message='This username is taken')

        return response

class ChatServiceServicer(chat_service_pb2_grpc.ChatServiceServicer):
    def SendMessage(self, request, context):

        sender = request.sender
        recipient = request.recipient
        content = request.content

        if sender not in db["passwords"] or recipient not in db["passwords"]:
            # send an error later
            return chat_service_pb2.SendResponse(success = False, message = "Invalid sender or recipient")

        print(f"Received message from {sender} to {recipient}: {content}")

        db["messages"][recipient].append(request)
        

        return chat_service_pb2.SendResponse(success = True, message = "Message sent")

    def GetUsers(self, request, context):
        for user in db["passwords"]:
            yield chat_service_pb2.User(username = user)
    
    def ReceiveMessage(self, request, context):
        recipient = request.username 

        for i in range(len(db["messages"][recipient]) - 1, -1, -1):
            message = db["messages"][recipient][i]
            yield chat_service_pb2.ChatMessage(sender = message.sender, content = message.content)
            db["messages"][recipient].pop()
            storeData(db)
        
                    


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_service_pb2_grpc.add_AuthServiceServicer_to_server(AuthServiceServicer(), server)
    chat_service_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()