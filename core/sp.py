import os
from collections import OrderedDict


from utils.global_functions import *
from utils.ci_pair import *

#from core.AbSp import *
from core.WriteManager import *

def search_list(val, l):
    for x in l:
        if isinstance(x,list):
            search_list(val, x)
        else:
            if isinstance(x, ci_pair):
                if x.class_name==val:
                    return True, x
            elif x==val:
                w
                return True, x
            else:
                pass
    return False, None

def get_file_path(f):
    file_path, dir_path = None, None
    for (path, direc, files) in os.walk(os.getcwd()):
        for filename in files:
            if filename == f:
                file_path = "{}/{}".format(path, filename)
                dir_path = "{}".format(path)
    try:
        return file_path, dir_path

    except UnboundLocalError:
        print("Cannot find the file \"{}\".".format(f))
        raise

def get_relative_path(source_file, target_file, virtual_source=False):
    if virtual_source == True:
        source_dir = source_file[::-1].split("/",1)[1][::-1]
    else:
        _, source_dir = get_file_path(source_file)
    target_path, _ = get_file_path(target_file + ".sp")
    relative_path = os.path.relpath(target_path, start=source_dir)
    return relative_path


class SP():
    def __init__(self, 
                 file_dir="./",
                 file_name="test",
                 file_type="module",
                 design=None,
                 design_args=None):
        """
        self.sub_inst:
            It collects the instances that were instanciated in this file.
            e.g., self.inst["rram"]=[inst_0, ...] (inst_0 is a reference for an instance)
        self.global_X:
            It collects the X (nodes, prameters) that were defined in this file.
            e.g., self.global_node["weight"]=[ci_pair("weight_0":"3")]
        """
        self.file_name = file_name
        self.file_dir = file_dir
        self.file_ext = ".sp"
        self.file_type = file_type
        self.file_path = file_dir + file_name + self.file_ext
        self.stmnt = OrderedDict({"include":[],
                                  "option":[],
                                  "temperature":[],
                                  "end":[]})
        self.cmd = OrderedDict({"include":".include",
                                "option":".option",
                                "temperature":".temp",
                                "parameter":".param",
                                "node":".glboal",
                                "inline":"+",
                                "end":".end",
                                "ends":".ends",
                                })

        self.sub_inst = OrderedDict({})
        self.global_node = OrderedDict({})
        self.global_param = OrderedDict({})
        if design==None:
            pass
        else:
            SP.design=design
            self.design(design_args)

    def _add_cmd(self, label, new_cmd=None):
        """
        Expand the command dictionary, cmd_dict, to cover a new cmd.
        """
        self.cmd_dict[label]=[]
        if new_cmd==None:
            stmnt = "." + label + " "
        else:
            stmnt = "." + new_cmd + " "
        self.cmd[label].append(stmnt)
        self.cmd[label].append([])

    def add_cmd(self, label, new_cmd=None):
        self._add_cmd(self, label, new_cmd)

    def write(self, is_topfile=False, alternate=-1, overwrite=False):
        """
        Write all things at the opened file.
        """
        if exist_file(self.file_dir, self.file_name + self.file_ext) != True or overwrite==True:
            self.wr_manager = WriteManager(file_type = self.file_type,
                                           file_object = self)
            self.wr_manager.write(alternate=alternate)
        else:
            print("No need to call write...")

#COFRIMED!
    def include_stmnt(self, stmnt, stmnt_val=None):
        """
        PARAMETERS:
        stmnt_type: the type of statement. refer to self.stmnt.keys()
        stmnt_var: the variable/file name for the given statement. will be stored at self.stmnt.values()
        stmnt_val: the value for the given variable. "include" are not allowed to be assigned.

        EXCEPTION:
        "include": Find the relative path from this file and store it into dict.
        """
        stmnt_type, stmnt_name = decipher(stmnt)
        # 0. Cofirm that the type of statement is allowed or not
        is_stmnt = stmnt_type in self.stmnt.keys()
        if is_stmnt == False:
            raise ValueError("The \"{}\" is not allowed statement.".format(stmnt_type))
        # 1. Assign variables/files with values to the corresponding types.
        if stmnt_val==None:
            if stmnt_type=="include":
                stmnt_name = get_relative_path(self.file_path, stmnt_name, virtual_source=True)
            else:
                pass
        else:
            if stmnt_type=="include":
                raise ValueError("The \".include\" is not allowed to have assigned value.")
            else:
                var = stmnt_name + "=" + str(stmnt_val)
        self.stmnt[stmnt_type].append(stmnt_name) 
   
    def _label_what(self, _name, shape, _set, _val):
        is_leaf = (len(shape) < 1)
        if is_leaf != True:
            _shape = shape[:]
            dim = _shape[0]
            _shape.pop(0)
            for i in range(dim):
                if _val != None:
                    __val = _val[i]
                _name_copied = (_name + ".")[:-1]
                _name_copied = _name_copied + "_" + str(i)
                self._label_what(_name_copied, _shape, _set, __val)
        else:
            if _val != None:
                _pair = ci_pair(class_name=_name, inst_name=_val)
            else:
                _pair = ci_pair(class_name=_name)
            _set.append(_pair)

    def _align_what(self, _set, _shape):
        return list_to_numpy(_set).reshape(_shape).tolist()

    def define_global(self, what, *shape, align=True, skip_exception=True, val=[]):
        """
        FUCNTION:
        This method define nodes/parameters for subckt module.

        PARAMETERS:
        1) what: str; "type:name"; the name of subckt node/parameters; e.g., nodes, parameters which are passed by.
        2) shape: tuple; (dim #1,...); the shape of nodes or parmeters labeling.
        3) align: bool; True/False; boolean variable to indicate whether reshape or not.
        4) skip_exception: bool; True/False; boolean variable whether to skip checking for exception.
        
        VARIABLES:
        ) _type, _name: the interpretation for a parameter, what.
        ) _set: it stands for self.node or self.parameter; _set[_name]=[] to store the node defined. 
        """
        # 0. Confirm that the defined node already exist or not.
        _type, _name = decipher(what)
        if skip_exception != True:
            is_allowed, _ = search_list(_type, ["node", "parameter"])
            if is_allowed != True:
                raise ValueError("The defined type, {}, is not allowed.".format(_type))

        if isinstance(val, np.ndarray):
            _val = numpy_to_list(val)
        else:
            _val = val

        if _type=="parameter":
            _set = self.global_param
        else:
            _set = self.global_node
            if len(val) > 0:
                raise ValueError("Nodes are not allowed to be assigned values.")
        is_exist, _ = search_list(_name, _set.keys())
        if is_exist != True:
            _set[_name]=[]
        else:
            raise ValueError("The name to define already exists.")

        _shape = list(shape)
        self._label_what(_name, _shape, _set[_name], _val)
        print(_set) 
        if align == True:
            self._align_what(_set[_name], _shape)

    def assign(self, p, val):
        bus, p = decipher(p)
        exist_param, param = search_list(p, list(self.global_param[bus]))
        if exist_param != True:
            raise ValueError("The parameter, {}, does not exist.".format(param))
        already_assigned = (param.inst_name != "0")
        if already_assigned == True:
            raise ValueError("The parameter, {}, to be assigned has already allocated.".format(param))
        else:
            param.inst_name = str(val) 

    def instanciate(self, inst, param=None):
        # 0. Confirm that the class module for required specs of instance exist or not:
        # if not exist with specific spec, raise error.
        is_new_module = not (inst.module_name in self.sub_inst.keys())
        if is_new_module==True:
            self.sub_inst[inst.module_name]=[]
        else:
            is_overlapped = inst in self.sub_inst[inst.module_name]
            if is_overlapped == True:
                raise ValueError("The name of the defined instance, {}, already exist.".format(inst.inst_name))
        self.sub_inst[inst.module_name].append(inst)
        if param != None:
            inst.param = inst.param + param


    def _print_dict(self, descpt, dic):
        print(descpt)
        for key, val in dic.items():
            print("--"+key + ":", end=" ")
            print(val)
            if isinstance(val, np.ndarray):
                print(val.shape)

    def print_stat(self):
        print("\n","="*20, "The information for SP file or module","="*20)
        self._print_dict("Statements", self.stmnt)
        self._print_dict("Global nodes", self.global_node) 
        self._print_dict("Global params", self.global_param)
        self._print_dict("Instances", self.sub_inst)
