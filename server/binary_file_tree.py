import hashlib, secrets
import os
from anytree import AnyNode, RenderTree, search

# REFERENCES: https://github.com/droid76/Merkle-Tree/blob/master/checkinclusion.py

# REFERENCES: https://gist.github.com/thinkphp/1472489


def get_list_of_files(dir_name):
    list_of_file = os.listdir(dir_name)
    all_files = list()
    for entry in list_of_file:
        full_path = os.path.join(dir_name, entry)
        if os.path.isdir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        else:
            all_files.append(full_path)
    return all_files 

def generate_file_info(filepath):
    f = open(filepath, "rb")
    filedata = f.read()
    h1 = hashlib.sha3_256(filedata)
    data_hash = h1.hexdigest()
    h2 = hashlib.sha3_256(str(filepath).encode())
    filepath_hash = h2.hexdigest()
    return [filepath_hash, filepath, data_hash]

def generate_all_files_info(path_folder):
    all_files = get_list_of_files(path_folder)
    info_list = []
    for f in all_files:
        info_list.append(generate_file_info(f))
    return info_list

# generate node with key: filepath_hash; value: [filepath, data_hash]
def generate_node(info_list, parent, i):
    info_element = info_list[0]
    if i==0:
        info_node = parent
    else:
        info_node = AnyNode(dict_keys=info_element[0], dict_values=[info_element[1], info_element[2]], parent=parent)
    i = i + 1           # indicates the level
    if len(info_list) > 1:
        info_list.remove(info_element)
        if len(info_list) == 1:
            generate_node(info_list=info_list, parent=info_node, i=i)
        elif len(info_list) > 1:
            first_half = info_list[:len(info_list)//2]
            second_half = info_list[:len(info_list)//2]
            generate_node(info_list=first_half, parent=info_node, i=i)
            generate_node(info_list=second_half, parent=info_node, i=i)
    return info_node

# return node with charged data from defined path_folder
def build_tree(path_folder):
    info_list = generate_all_files_info(path_folder)
    parent = AnyNode(dict_keys=info_list[0][0], dict_values=[info_list[0][1], info_list[0][2]], parent=None)
    node = generate_node(info_list=info_list, parent=parent, i=0)
    return node

# returns an array that contains all info by filepath_hash
def search_values(node, filepath_hash):
    [filepath, data_hash] = search.find_by_attr(node,name='dict_keys',value=filepath_hash).dict_values
    return [filepath_hash, filepath, data_hash]


# TEST PART
principal_node = build_tree('client/files')
filepath_example_hash = '72d7984af6f5aa0ae36e7868f8c025c73cf5003df9d41788fef6a19c2e721a36'
[filepath_hash, filepath, data_hash] = search_value(node=principal_node, filepath_hash=filepath_example_hash)
print('Search filepath_hash by a_value: ', filepath_hash)
print('Search filepath by a_value: ', filepath)
print('Search data_hash by a_value: ', data_hash)
