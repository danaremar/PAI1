import hashlib
import os
import secrets
#import glob
#import random


def get_list_of_files(dir_name):

    # create a list of file and sub directories 
    # names in the given directory 
    list_of_file = os.listdir(dir_name)
    all_files = list()

    # Iterate over all the entries
    for entry in list_of_file:

        # Create full path
        full_path = os.path.join(dir_name, entry)

        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        else:
            all_files.append(full_path)
                
    return all_files      



def generate_file_verification(filepath):

    f = open(filepath, "rb")
    filedata = f.read()
    h = hashlib.sha3_256(filedata)
    hash_value = h.hexdigest()

    file_name = filepath.split("\\")[-1]

    #token = random.getrandbits(256)
    n_bits = 256
    token = secrets.token_hex(int(n_bits/8))

    return [file_name, hash_value, token]



def generate_all_files_verification(path_folder):

    # generate a list of file paths
    all_files = get_list_of_files(path_folder)              #   -> FULL RECURSIVE
    #all_files = glob.glob(path_folder+'/**', recursive=True)   -> RECURSIVE WITH EXPRESSION (return base folder too)
    #all_files = os.listdir(path_folder)                        -> ONLY RETURNS FROM BASE FOLDER

    # generate file verification
    verifications = []
    for f in all_files:
        verifications.append(generate_file_verification(f))
    return verifications



def print_files_verification(verifications):
    for f in verifications:
        print('File:', f[0], ', hash:', f[1], ' token:', f[2])


#############################################################################################################
############################################  TESTS  ########################################################
#############################################################################################################

path_folder = 'client/files'
verifications = generate_all_files_verification(path_folder)
print_files_verification(verifications)


    








