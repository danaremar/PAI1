import socket
import json

HOST = '127.0.0.1'
PORT = 55333

def dummy_verification(filename, hash_file, token):
    return "OK"

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

                        response = {"hash": hash_file, "response": dummy_verification(filename, hash_file, token)}
                        dumped_response = json.dumps(response)
                        conn.sendall(bytes(dumped_response, encoding="utf-8"))

                s.close()

server = HIDSServer(HOST, PORT)
server.run()