from sys import hash_info
from typing import List
from decouple import config
import json
import os

# INPUT: file_name, the name of the file in the folder /files/to_adjust/
# OUTPUT: If there was an error opening the file, return "Error", else return the ["data"][0] of the json
def save_data_json(file_name, tag = "data"):
    try:
        with open (file_name) as json_file:
            file = json.load(json_file)
            return file[tag]
    except Exception as e:
        return "Error"

# INPUT: 
    # file_name, the name of the file in the folder /files/to_adjust/
    # start, the initial string
# OUTPUT: If there was an error opening the file, return start, else add the data to the tail of start
def concat_files(file_name, start = [], tag = "data"):
    data_file = save_data_json(file_name, tag)

    if data_file != "Error":
        start.extend(data_file)
        return start
    else:
        return start

# INPUT: 
    # initial, the inital part to search with ls
    # extension, the extension to search for
# OUTPUT: list of string containg all file full path
def list_of_file_name_from_initial(initial, extension = ""):
    return os.popen('ls '+ initial + "*" + extension).read().splitlines()

# INPUT:
    # name, the name to search in "/files/to_adjust/" to obtain the list of file
    # json_tag, the json tag that i want to concat
# OUTPUT: a file in "/files/" containing the concatenation of that json tag for alle the file with that name
def concat_json_tag_from_part_name(name, json_tag = "data"):
    name = os.getcwd() + "/files/to_adjust/" + name
    list_of_file_name = list_of_file_name_from_initial(name, ".json")

    element_json_list = []

    for file in list_of_file_name:
        element_json_list = concat_files(file, element_json_list, 'data')

    json_string = {json_tag : element_json_list}

    name = name.replace('to_adjust/','')

    with open(name + '.json', 'w') as outfile:
        json.dump(json_string, outfile)


print('Write the invariant part of the name of the file')
file_name = input()
while file_name == '':
    print('Try better') 
    file_name = input()

concat_json_tag_from_part_name(file_name)