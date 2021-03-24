import socket
import json
import hashlib
from file_service import generate_all_files_verification
from hmac_generator import generate_hmac
from scheduler import CustomScheduler
from schedule import Scheduler
import conf
from custom_logger import warning, info


HOST = conf.SERVER_IP
PORT = conf.SERVER_PORT
DEBUG_MODE = conf.DEBUG_MODE
ALWAYS_CORRECT = DEBUG_MODE and conf.ALWAYS_CORRECT
FAST_LOOP = DEBUG_MODE and conf.FAST_LOOP
SECRET = conf.SECRET
SCAN_DIRECTORY = conf.SCAN_DIRECTORY
FRECUENCY = conf.HOUR_FRECUENCY


def create_challenge(token):
    t1 = int(token, 16) % SECRET*7
    t2 = int(token, 16) % SECRET
    challenge = t1*t2
    return challenge

class HIDSClient:

    def __init__(self, host='127.0.0.1', port=55333):
        self.host = host
        self.port =  port
    
    def request_verification(self, filepath_hash, data_hash, token):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            data = {"filepath_hash" : filepath_hash, "data_hash": data_hash, "token": token}
            dumped_data = json.dumps(data)
            
            s.sendall(bytes(dumped_data, encoding="utf-8"))
            response = s.recv(1024)
            return response

    def request_all_verifications(self, path_folder):
        info('Starting verification')
        verifications = generate_all_files_verification(path_folder)
        num_error = 0
        num_files = len(verifications)
        for i in verifications:
            [filepath_hash, filepath, data_hash, token] = i
            json_response = self.request_verification(filepath_hash, data_hash, token)
            response = json.loads(json_response.decode('utf8'))
            if response["response"]["verification"] == "VERIFICATION_SUCCESS":
                final_verification = self.file_verification(filepath, data_hash, token, response["response"]["MAC"], response["response"]["file_token_hash"])
                if not final_verification:
                    warning(f'VERIFICATION FAILURE: Filepath: {filepath}')
                    num_error = num_error+1
            else:
                warning(f'VERIFICATION FAILURE: Filepath: {filepath}')
                num_error = num_error+1
        info('Ending verification')
        
        
        info(f'Summary: {num_files} files verified. {num_error} failures. {round((num_error/num_files)*100, 2)}% of integrity errors')
                

    def file_verification(self, filepath, expected_hash, token, server_hmac, file_token_hash_received):
        challenge = create_challenge(token)
        mac_file = generate_hmac(expected_hash, token, challenge)
        file_token_hash_client = self.get_file_token_hash(filepath,token)
        return mac_file == server_hmac and file_token_hash_client == file_token_hash_received

    def get_file_token_hash(self, filepath, token):
        f = open(filepath, "rb")
        filedata = f.read()
        h1 = hashlib.sha3_256(filedata + bytearray.fromhex(token))
        file_token_hash = h1.hexdigest()
        return file_token_hash


if __name__ == "__main__":
    client = HIDSClient(HOST, PORT)
    
    #Creación del scheduler
    schedule1 = Scheduler()

    #Define frecuencia y método a ejecutar
    if FAST_LOOP:
        info("Debugger fast loop active. Executing every 15 seconds")
        schedule1.every(15).seconds.do(client.request_all_verifications, SCAN_DIRECTORY)
    else:
        info(f"Executing every {FRECUENCY} hours")
        schedule1.every(FRECUENCY).hours.do(client.request_all_verifications, SCAN_DIRECTORY)
    
    sched1 = CustomScheduler(schedule1)
    sched1.threaded_schedule()

    #Primera ejecución
    client.request_all_verifications(SCAN_DIRECTORY)

    while True:
        pass



