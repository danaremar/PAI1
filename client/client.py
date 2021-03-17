import socket
import json

class HIDSClient:
    def __init__(self, host='127.0.0.1', port=55333):
        self.host = host
        self.port =  port
    
    def request_verification(self, filename, hash, token):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            data = {"filename" : filename, "hash": hash, "token": token}
            dumped_data = json.dumps(data)

            s.sendall(bytes(dumped_data, encoding="utf-8"))
            response = s.recv(1024)
            print('Received', repr(response))
            

# EJEMPLO DE USO: Los valores para host y port son opcionales
#client = HIDSClient('127.0.0.1', 55333)
#client.request_verification("FILENAME","hash","token")




