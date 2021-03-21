import socket
import json
from file_service import generate_all_files_verification, print_verification
from hmac_generator import generate_hmac

def dummy_callenge(token):
    return "challenge"

def file_verification(filename, expected_hash, token, server_hmac):
    challenge = dummy_callenge(token)
    mac_file = generate_hmac(expected_hash, token, challenge)
    return mac_file == server_hmac

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
            return response

    def request_all_verifications(self, path_folder):
        verifications = generate_all_files_verification(path_folder)
        for i in verifications:
            print_verification(i)
            [filename, hash_file, token] = i
            json_response = self.request_verification(filename, hash_file, token)
            response = json.loads(json_response.decode('utf8'))
            if response["response"]["verification"] == "VERIFICATION_SUCCES":
                print(file_verification(filename,hash_file, token, response["response"]["MAC"]))
            else:
                print(response["response"]["verification"])


# EJEMPLO DE USO: Los valores para host y port son opcionales
if __name__ == "__main__":
    client = HIDSClient('127.0.0.1', 55333)
    client.request_all_verifications("client/files")




