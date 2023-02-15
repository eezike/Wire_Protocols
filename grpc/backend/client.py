import grpc
import myservice_pb2
import myservice_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
authstub = myservice_pb2_grpc.AuthServiceStub(channel)
messagestub = myservice_pb2_grpc.MessageServiceStub(channel)

username = input("Username: ")
password = input("Password: ")

request = myservice_pb2.RegisterRequest(username=username, password=password)
response = authstub.Register(request)

if response.success:
    print(response.message)
else:
    print(response.message)


username = input("Username: ")
password = input("Password: ")

request = myservice_pb2.LoginRequest(username=username, password=password)
response = authstub.Login(request)

if response.success:
    print(response.message)
else:
    print(response.message)

'''
import grpc
import example_pb2
import example_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        calculator_stub = example_pb2_grpc.CalculatorStub(channel)
        weather_forecast_stub = example_pb2_grpc.WeatherForecastStub(channel)

        # Call the Add method of the Calculator service
        add_request = example_pb2.AddRequest(num1=3, num2=4)
        add_response = calculator_stub.Add(add_request)
        print(f"Result of 3 + 4 = {add_response.result}")

        # Call the Subtract method of the Calculator service
        subtract_request = example_pb2.SubtractRequest(num1=5, num2=2)
        subtract_response = calculator_stub.Subtract(subtract_request)
        print(f"Result of 5 - 2 = {subtract_response.result}")

        # Call the GetCurrentWeather method of the WeatherForecast service
        weather_request = example_pb2.GetCurrentWeatherRequest()
        weather_response = weather_forecast_stub.GetCurrentWeather(weather_request)
        print(f"Current weather conditions: {weather_response.conditions}, temperature: {weather_response.temperature} F")

        # Call the GetWeatherForecast method of the WeatherForecast service
        forecast_request = example_pb2.GetWeatherForecastRequest()
        forecast_response = weather_forecast_stub.GetWeatherForecast(forecast_request)
        print("3-day weather forecast:")
        for day, forecast in enumerate(forecast_response.forecast):
            print(f"Day {day+1}: High temperature {forecast.high_temperature} F, low temperature {forecast.low_temperature} F, conditions: {forecast.conditions}")

if __name__ == '__main__':
    run()
'''