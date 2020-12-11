from collections import OrderedDict
import numpy as np

from core.sp import *
from utils.global_functions import *

def init_param(s, init_value=0):
    return s + "=" + str(init_value)

def search_list(val, l):
    for x in l:
        if isinstance(x,list):
            search_list(val, x)
        else:
            if isinstance(x, ci_pair):
                if x.class_name==val:
                    return True, x
            elif x==val:
                return True, x
            else:
                pass
    return False, None

class Module(SP):
    def __init__(self, 
                 module_name,
                 inst_name,
                 file_dir="./", 
                 design=None,
                 design_args=None):
        """
        FUNCTION:


        PARAMETERS:
        module_name(inst_name): the module class (instance) name of subckt.
        design, design_args: the netlist function of each module and required arguments. 

        VARIABLES:
        self.node:
            It collects nodes which are defined for a subckt.
            e.g., self.node[node_bus] = [ci_pair,...] (list type)
        self.param:
            It collects params which are defined for a subckt.
            e.g., self.param[param_bus] = [ci_pair,...] 
        """
        self.module_name, self.module_type, self.inst_name = module_name, None, inst_name
        self.node, self.param, self.function = OrderedDict({}), OrderedDict({}), OrderedDict({})
        super(Module, self).__init__(file_dir=file_dir, 
                                     file_name=module_name,
                                     file_type="module",
                                     design=None)

        self.random_cnt = 0
        self.random_node = inst_name + "_Node_" + str(self.random_cnt)

        basic_module_set = {"voltage":"v", "resistor":"r", "capacitor":"d",}
        self.module_type = "custom" if exist_file(dir_path=file_dir, f=self.file_name+".sp") else None
        self.module_type = "basic" if module_name[0] in basic_module_set.values() else self.module_type
        if self.module_type == "basic":
            self.prefix = module_name[0]
        else:
            self.prefix = "x"
            self.inst_name = self.prefix + self.inst_name

        if design==None:
            if self.module_type == "custom":
                file_path, dir_path = get_file_path(self.file_name+".sp")
                self._browse_custom_module(file_path)
            else:
                raise ValueError("The module, {}, does not exist. Compose design function or .sp file".format(module_name))
        else:
            if self.module_type==None:
                self.module_type = "new"
            Module.design = design
            if design_args==None:
                self.design()
            else:
                self.design(design_args)


    def _detect_node_param(self, word_list):
        for word in word_list:
            if word.find("=") > -1:
                _name, _val = word.split("=")
                self.define_local("parameter:"+_name, val=_val)
            else:
                _name = word
                self.define_local("node:"+_name)

    def _browse_custom_module(self, file_path):
        f = open(file_path, "r")
        read_once = False
        for line in f.readlines():
            if line.find(".subckt") > -1 and not read_once:
                word_list = line.strip("\n").split(" ")
                for idx, word in enumerate(word_list):
                    if word == ".subckt":
                        self.module_name = word_list[idx+1]
                        break
                self._detect_node_param(word_list[idx+2:])
                print("ECK:",word_list)

            elif line.find("+") > -1 and not read_once:
                word_list = line.lstrip("+").rstrip("\n").strip(" ").split(" ")
                self._detect_node_param(word_list)
            elif line.find(".ends") > -1:
                read_once = True

### Start: Methods for "define_what(...)"
    def _label_what(self, _name, shape, _set, _val):
        if len(shape)>0:
            _shape = shape[:]
            dim = _shape[0]
            _shape.pop(0)
            for i in range(dim):
                if len(_val) > 0:
                    _val = _val[i]
                _name_copied = (_name + ".")[:-1]
                _name_copied = _name_copied + "_" + str(i)
                self._label_what(_name_copied, _shape, _set, _val)
        else:
            if _val != []:
                _pair = ci_pair(class_name=_name, inst_name=_val)
            else:
                _pair = ci_pair(class_name=_name)
            _set.append(_pair)

    def _align_what(self, _set, _shape):
        return list_to_numpy(_set).reshape(_shape).tolist()

    def define_local(self, what, *shape, align=True, skip_exception=True, val=[]):
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

#        if isinstance(val, int):
#            _val = val
#        elif val != None:
#            _val = list(val)
#        else:
#            pass
        _val = val

        if _type=="parameter":
            _set = self.param
        elif _type=="node":
            _set = self.node
            if len(val) > 0:
                raise ValueError("Nodes are not allowed to be assigned values.")
        elif _type=="function":
            _set = self.function
        is_exist, _ = search_list(_name, _set.keys())
        if is_exist != True:
            _set[_name]=[]
        else:
            raise ValueError("The name, {}, to define already exists.".format(_name))

        _shape = list(shape)
        print(_name, _shape)
        self._label_what(_name, _shape, _set[_name], _val)
        
        if align == True:
            self._align_what(_set[_name], _shape)
### End: Methods for "define_what(...)"

### Start: Methods for "generate(...)/instanciate(...)"
    def write(self, overwrite=False):
        allowed_module_type = False if self.module_type in ["basic","custom"] else True
        print(self.module_name, ":::::: ", allowed_module_type)
        if allowed_module_type == True:
            super(Module, self).write(overwrite=overwrite)

### End: Methods for "generate(...)/instanciate(...)"

### Start: Methods for "connect(...)"
    def connect(self, m1, n1, m2, n2, node_name=None):
        bus1, n1 = decipher(n1)
        bus2, n2 = decipher(n2)
        # 0. Confirm that 1)
        inst1_set = [self] if m1==self else self.sub_inst[m1.module_name]
        inst2_set = [self] if m2==self else self.sub_inst[m2.module_name]
        exist_inst1, inst1 = search_list(m1, inst1_set)
        exist_inst2, inst2 = search_list(m2, inst2_set)
        exist_inst = exist_inst1 and exist_inst2
        if exist_inst != True:
            raise ValueError("The instance,  error")
        exist_node1, node1 = search_list(n1, list(m1.node[bus1]))
        exist_node2, node2 = search_list(n2, list(m2.node[bus2]))
        exist_node = exist_node1 and exist_node2
        if exist_node != True:
            if exist_node1 != True:
                raise ValueError("The node, {}, does not exist.".format(node1.class_name))
            if exist_node2 != True:
                raise ValueError("The node, {}, does not exist.".format(node2.class_name))
        # 1. 
        have_self = (self==m1) or (self==m2)
        if have_self==True:
            if self==m2:
                tmp_m, tmp_n, tmp_node = m1, n1, node1
                m1, n1, node1 = m2, n2, node2
                m2, n2, node2 = tmp_m, tmp_n, tmp_node
            node_name = node1.class_name
            node2.inst_name = node_name
        else:
            already_defined = (node1.inst_name != "0") and (node2.inst_name != "0")
            print(m1.inst_name, node1.class_name, node1.inst_name, " || ",m2.inst_name, node2.class_name, node2.inst_name, " || ", node_name)
            if already_defined == True:
                if node_name != None:
                    raise ValueError("The node is already defined. Overwrited.")
                if node1.inst_name != "0":
                    node_name = node1.inst_name
                else:
                    node_name = node2.inst_name
            else:
                if node_name==None:
                    node_name = self.random_node
                    self.random_cnt += 1
            node1.inst_name, node2.inst_name = node_name, node_name

    def assign(self, m, p, p_assgn):
        exist_inst, inst = search_list(m, self.sub_inst[m.module_name])
        if exist_inst != True:
            raise ValueError("The instance, {}, does not exist.".format(inst))
        bus, p = decipher(p)
        bus_assgn, p_assgn = decipher(p_assgn)
        exist_param_l, param_l = search_list(p, list(m.param[bus]))
        exist_param_assgn, param_assgn = search_list(p_assgn, list(OrderedDict(self.global_param, **self.param)[bus_assgn]))
        exist_param = exist_param_l and exist_param_assgn
        if exist_param != True:
            if exist_param_l != True:
                raise ValueError("The parameter, {}, does not exist.".format(param_l))
            if exist_param_assgn != True:
                raise ValueError("The parameter, {}, does not exist.".format(param_assgn))

        already_assigned = (param_l.inst_name != "0")
        if already_assigned == True:
            raise ValueError("The parameter, {}, to be assigned has already allocated with a value.".format(param_l))
        else:
            param_l.inst_name = param_assgn.class_name

### End: Methods for "connect(...)"
    def print_stat(self):
        super(Module, self).print_stat()
        print("Module: ", self.module_name, ":", self.inst_name , "("+self.module_type+")")
        self._print_dict("Nodes", self.node)
        self._print_dict("Params", self.param)
        print("="*60)
