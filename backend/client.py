# dhcp-10-250-150-39.harvard.edu
# DESKTOP-EUAUCFM
# Victor: 10.250.235.165
# Emeka: 10.250.150.39
# Python program to implement client side of chat room.
import socket
import threading
import backend.wireprotocol as wp

class Client:
    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self, host="10.228.185.36", port=9999):
        if not self.connected:
            try:
                self.clientsocket.connect((host, port))
                if self.receive_response() == wp.RESPONSE_CODE.WELCOME:
                    self.connected = True
            except:
                pass

        return self.connected

    def send_login(self, username, password):
        wp.sendone(self.clientsocket, wp.MSG_TYPES.LOGIN, username = username, password = password)
        return self.receive_response()

    def send_register(self, username, password):
        wp.sendone(self.clientsocket, wp.MSG_TYPES.REGISTER, username = username, password = password)
        return self.receive_response()
    
    def send_message(self, _to, _from, body):
        wp.sendone(self.clientsocket, wp.MSG_TYPES.SEND_MSG, _from = _from, _to = _to, body = body)
    
    def get_users(self):
        wp.sendone(self.clientsocket, wp.MSG_TYPES.RESPONSE, response_code = wp.RESPONSE_CODE.REQ_USERS)
        return self.receive_response()

    def receive_response(self):
        try:
            message_type, payload = wp.receive_message(self.clientsocket)
            if message_type == wp.MSG_TYPES.RESPONSE:
                response_code = wp.unpack_payload(message_type, payload)
                return response_code
            elif message_type == wp.MSG_TYPES.RES_USERS:
                user = wp.unpack_payload(message_type, payload)
                if user != "":
                    return [user] + self.receive_response()
                else:
                    return []
            else:
                print("Error 1")
            
        except:
            print("Error 2")
            pass
            
        return wp.RESPONSE_CODE.UNKNOWN_ERROR