import socket
import json
from binary_file_tree import search_value
from hmac_generator import generate_hmac

HOST = '127.0.0.1'
PORT = 55333
ALWAYS_CORRECT = True

def dummy_verification(filename, hash_file, token):
    return "OK"

def dummy_callenge(token):
    return "challenge"

#TODO: Construir correctamente el path
def get_file_path(filename):
    return f"files/{filename}"

def file_verification(filename, hash_file, token):
    #TODO: Como se hacen búsquedas en el arbol de verdad?
    hash_value = search_value(filename)
    mac_file = None
    verification = "VERIFICATION_FAILED"
    if (hash_file == hash_value) or ALWAYS_CORRECT:
        challenge = dummy_callenge(token)
        mac_file = generate_hmac(hash_file, token, challenge)
        verification = "VERIFICATION_SUCCES"
    
    return {"verification":verification, "MAC":mac_file}



class HIDSServer:
    def __init__(self, host='127.0.0.1', port=55333):
        self.host = host
        self.port =  port

    def run(self):
        while (True):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        print(data)
                        verification = json.loads(data)
                        filename = verification["filename"]
                        hash_file = verification["hash"]
                        token = verification["token"]
                        print('SERVER - File:', filename, ', hash:', hash_file, ' token:', token)

                        response = {"hash": hash_file, "response": file_verification(filename, hash_file, token)}
                        dumped_response = json.dumps(response)
                        conn.sendall(bytes(dumped_response, encoding="utf-8"))

                s.close()

server = HIDSServer(HOST, PORT)
server.run()