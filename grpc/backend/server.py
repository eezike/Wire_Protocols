import grpc
from concurrent import futures
import myservice_pb2
import myservice_pb2_grpc
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
            "messages": [],
            "from_messages" : dict()
        }
    
    return db

db = loadData()



class AuthServiceServicer(myservice_pb2_grpc.AuthServiceServicer):
    def Login(self, request, context):
        if request.username in db["passwords"] and request.password == db["passwords"][request.username]:
            response = myservice_pb2.LoginResponse(success=True, message='Login successful')
            stream = context.otherside_context().wrap(grpc.server_streaming).invoke_rpc()
            db["active_streams"][request.username] = stream
            storeData(db)

            for message in db["messages"]:
                if message.recipient_username == request.username:
                    stream.send_message(message)

        else:
            response = myservice_pb2.LoginResponse(success=False, message='Invalid username or password')
        return response
    
    def Register(self, request, context):
        if request.username not in db["passwords"]:
            response = myservice_pb2.LoginResponse(success=True, message='Register successful')
            db["passwords"][request.username] = request.password
            stream = context.otherside_context().wrap(grpc.server_streaming).invoke_rpc()
            db["active_streams"][request.username] = stream
            storeData(db)
        else:
            response = myservice_pb2.LoginResponse(success=False, message='This username is taken')
        return response

'''
import grpc
from concurrent import futures
import example_pb2
import example_pb2_grpc

class CalculatorServicer(example_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        result = request.num1 + request.num2
        return example_pb2.AddResponse(result=result)

    def Subtract(self, request, context):
        result = request.num1 - request.num2
        return example_pb2.SubtractResponse(result=result)

class WeatherForecastServicer(example_pb2_grpc.WeatherForecastServicer):
    def GetCurrentWeather(self, request, context):
        conditions = "Sunny"
        temperature = 72
        return example_pb2.GetCurrentWeatherResponse(conditions=conditions, temperature=temperature)

    def GetWeatherForecast(self, request, context):
        forecast1 = example_pb2.WeatherDayForecast(high_temperature=75, low_temperature=62, conditions="Sunny")
        forecast2 = example_pb2.WeatherDayForecast(high_temperature=72, low_temperature=60, conditions="Cloudy")
        forecast3 = example_pb2.WeatherDayForecast(high_temperature=68, low_temperature=58, conditions="Rainy")
        forecast = [forecast1, forecast2, forecast3]
        return example_pb2.GetWeatherForecastResponse(forecast=forecast)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    example_pb2_grpc.add_WeatherForecastServicer_to_server(WeatherForecastServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
'''