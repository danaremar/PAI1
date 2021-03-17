import socket
import hashlib
import json

HOST = '127.0.0.1'
PORT = 55333

FILENAME = "client/files/example.txt"

def hash_file(file):
    return "12345"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    f = open(FILENAME, "rb")
    file_data = f.read()

    #data = {"filename" : FILENAME, "file": file_data, "hash":hash_file(file_data), "token":"token"}
    #dumped_data = json.dumps(data)

    #s.sendall(bytes(dumped_data, encoding="utf-8"))
    s.sendall(file_data)
    data = s.recv(1024)

    


print('Received', repr(data))



