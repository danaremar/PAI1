import socket

HOST = '127.0.0.1'
PORT = 55333

FILENAME = "files/example.txt"

while (True):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            f = open(FILENAME, "wb")
            while True:
                data = conn.recv(1024)
                while data:
                    f.write(data)
                if not data:
                    break
                #conn.sendall(data)
