import socket
import json

HOST = '127.0.0.1'
PORT = 55333

while (True):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                print(data)
                verification = json.loads(data)
                filename = verification["filename"]
                hash_file = verification["hash"]
                token = verification["token"]
                print('SERVER - File:', filename, ', hash:', hash_file, ' token:', token)

                if not data:
                    break
                conn.sendall(data)

        s.close()
