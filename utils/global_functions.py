import os
import sys
import errno

import string
import argparse

import numpy as np
from math import ceil



# global functions

####################
# GLOBAL FUNCTIONS #
####################

def make_node(s,*coord):
    node = s
    for i in coord:
        node = node + "_{}".format(i)
    return node

def init_param(s, init_value=0):
    return s + "=" + str(init_value)

def list_to_numpy(l):
    return np.array(l)

def numpy_to_list(arr):
    return arr.tolist()

def browse_custom_spfiles(path_f):
# read the file and tranform into a string
    sp_f = open(path_f, "r")
    file_contents = str(sp_f.read())

# read the module name of  memory element
    class_name = None
    sp_f = open(path_f, "r")
    split_line = list()
    for line in sp_f:
        if line.find(".subckt") > -1:
            split_line = line.split(" ")
            for idx, words in enumerate(split_line):
                if words == ".subckt":
                    indicator = idx+1
                    class_name = split_line[indicator]
                    break
            break
    print("The element of memory: ", class_name)

    return class_name, file_contents

def get_file_path(f):
    for (path, direc, files) in os.walk(os.getcwd()):
        for filename in files:
            if filename == f:
                file_path = "{}/{}".format(path, filename)
                dir_path = "{}".format(path)
    try:
        return file_path, dir_path

    except UnboundLocalError as e:
    #    sys.tracebacklimit = None
        print("Cannot find the file \"{}\".".format(f))
        raise

def exist_file(dir_path, f):
    for (path, _, files) in os.walk(dir_path):
        for file_name in files:
            if file_name == f:
                return True 
    return False

def include_spfiles(source_file, target_file, is_source_confirmed=False):
    if is_source_confirmed is False:
        _, source_path = get_file_path(source_file)
    else:
        source_path = source_file
    target_path, _ = get_file_path(target_file)
    path = os.path.relpath(target_path, start=source_path)
    return "\n"+".include " + path

def make_dir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return

curr_path = None
def change_dir(new_path):
    global curr_path
    curr_path = os.getcwd()
    os.chdir(new_path)
    return

def rechange_dir():
    global curr_path
    os.chdir(curr_path)
    curr_path = None
    return

def make_spfile(dir_path, module_name, is_module = True):
    path = dir_path + module_name + ".sp"
    f = open(path, "w")
    if is_module is True:
        f.write("\n" + ".subckt " + module_name)
    else:
        f.write("\n")
    return f


def save_numpy(dir_path, file_name, arr):
    path = dir_path + file_name
    return np.save(path, arr)

def load_numpy(dir_path, file_name):
    return np.load(dir_path+file_name, allow_pickle=True)

def enroll_custom_spfiles():
    return

def transform_bias(bias):
    

    return transformed_bias

def decipher(s):
    if s.find(":") > -1:
        s_list = s.split(":")
        key, val = s_list[0], s_list[1]
        if s_list[1]=="":
            val = key
        return key, val
    else:
        return s

