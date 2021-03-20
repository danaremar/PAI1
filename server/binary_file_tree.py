import hashlib, secrets
import os
from anytree import AnyNode, RenderTree, search

# REFERENCES: https://github.com/droid76/Merkle-Tree/blob/master/checkinclusion.py

# REFERENCES: https://gist.github.com/thinkphp/1472489


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



def generate_file_info(filepath):

    f = open(filepath, "rb")
    filedata = f.read()
    h = hashlib.sha3_256(filedata)
    hash_value = h.hexdigest()

    file_name = filepath.split("\\")[-1]

    return [file_name, hash_value, f.read]



def generate_all_files_info(path_folder):
    # generate a list of file paths
    all_files = get_list_of_files(path_folder)              #   -> FULL RECURSIVE
    #all_files = glob.glob(path_folder+'/**', recursive=True)   -> RECURSIVE WITH EXPRESSION (return base folder too)
    #all_files = os.listdir(path_folder)                        -> ONLY RETURNS FROM BASE FOLDER

    # info_list file verification
    info_list = []
    for f in all_files:
        info_list.append(generate_file_info(f))
    return info_list



def generate_node(info_list, parent, i):

    info_element = info_list[0]
    if i==0:
        info_node = parent
    else:
        info_node = AnyNode(dict_keys=[info_element[0], info_element[1]], dict_values=info_element[2], parent=parent)
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



def build_tree(path_folder):
    
    info_list = generate_all_files_info(path_folder)
    parent = AnyNode(dict_keys=[info_list[0][0], info_list[0][1]], dict_values=info_list[0][2], parent=None)
    node = generate_node(info_list=info_list, parent=parent, i=0)
    return node

    

# TEST PART

# WITH FUNCTIONS
a = generate_all_files_info('client/files')
principal_node = build_tree('client/files')
print('Represents the tree: ', RenderTree(principal_node).by_attr('dict_keys'))

# MANUAL
# a = generate_all_files_info('client/files')
# a_value = [a[0][0],a[0][1]]
# b_value = [a[1][0],a[1][1]]
# a_tree = AnyNode(dict_keys=a_value, dict_values=a[0][2])
# b_tree = AnyNode(dict_keys=b_value, dict_values=a[1][2], parent=a_tree)
# print('Represents the tree: ', RenderTree(a_tree).by_attr('dict_keys'))
# print('Search by a_value: ', search.find_by_attr(a_tree,name='dict_keys',value=a_value))
