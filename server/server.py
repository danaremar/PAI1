import socket
import json
import hashlib
from binary_file_tree import search_values, build_tree
from hmac_generator import generate_hmac

HOST = '127.0.0.1'
PORT = 55333
ALWAYS_CORRECT = False
SECRET = 104723

def create_challenge(token):
    print('TOKEN', token)
    t1 = int(token, 16) % SECRET*7
    t2 = int(token, 16) % SECRET
    challenge = t1*t2
    print('CHALLENGE', challenge)
    return challenge

def get_file_token_hash(filepath, token):
    f = open(filepath, "rb")
    filedata = f.read()
    h1 = hashlib.sha3_256(filedata + bytearray.fromhex(token))
    file_token_hash = h1.hexdigest()
    return file_token_hash

class HIDSServer:
    def __init__(self, path, host='127.0.0.1', port=55333):
        self.host = host
        self.port =  port
        self.tree = build_tree(path)

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
                        filepath_hash = verification["filepath_hash"]
                        data_hash = verification["data_hash"]
                        token = verification["token"]
                        print('SERVER - filepath_hash:', filepath_hash, ', data_hash:', data_hash, ' token:', token)
                        resp = self.file_verification(filepath_hash, data_hash, token)

                        response = {"filepath_hash": filepath_hash, "response": resp}
                        dumped_response = json.dumps(response)
                        conn.sendall(bytes(dumped_response, encoding="utf-8"))

                s.close()

    def file_verification(self, filepath_hash, data_hash, token):
        verification = "VERIFICATION_FAILED"
        mac_file = None
        file_token_hash = None
        
        
        [file_filepath_hash, filepath, file_data_hash] = search_values(self.tree, filepath_hash)
        file_token_hash = get_file_token_hash(filepath, token)
        if (data_hash == file_data_hash) or ALWAYS_CORRECT:
            challenge = create_challenge(token)
            mac_file = generate_hmac(file_data_hash, token, challenge)
            verification = "VERIFICATION_SUCCESS"
        return {"verification":verification, "MAC":mac_file, "file_token_hash": file_token_hash}

if __name__ == "__main__":
    server = HIDSServer("./server/files", HOST, PORT)
    server.run()