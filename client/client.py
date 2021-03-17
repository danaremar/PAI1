import socket
import json
from file_service import generate_all_files_verification, print_verification

class HIDSClient:

    def __init__(self, host='127.0.0.1', port=55333):
        self.host = host
        self.port =  port
    
    def request_verification(self, filename, hash_file, token):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            data = {"filename" : filename, "hash": hash_file, "token": token}
            dumped_data = json.dumps(data)
            
            s.sendall(bytes(dumped_data, encoding="utf-8"))
            response = s.recv(1024)
            print('Received', repr(response))

    def request_all_verifications(self):
        path_folder = 'client/files'
        verifications = generate_all_files_verification(path_folder)
        for i in verifications:
            print_verification(i)
            [filename, hash_file, token] = i
            self.request_verification(filename, hash_file, token)


# EJEMPLO DE USO: Los valores para host y port son opcionales
client = HIDSClient('127.0.0.1', 55333)
client.request_all_verifications()




