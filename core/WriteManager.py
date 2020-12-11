from utils.ci_pair import *
#from core.spmodule import *

class WriteManager():
    def __init__(self, file_type, file_object):
        allowed_types = ["top", "data", "module"]
        self.file_type, self.obj = file_type, file_object
        self.file_path, self.file_name = self.obj.file_path, self.obj.file_name
        # open file
        with open(self.file_path, "w+") as file_handler:
            self.line_handler = file_handler.readlines()
        self.line_idx = 0

    def w_line(self, s):
        print(self.line_idx, ":", s)
        self.line_handler.insert(self.line_idx, s + "\n")
        self.line_idx = self.line_idx+1

    def w_list(self, l, elem_type, cmd):
        s = ""
        for x in l:
            if isinstance(x, list):
                w_list(sub_l, elem_type=elem_type)
            elif isinstance(x, ci_pair):
                if elem_type == "node_class":
                    s += (str(x.class_name))
                elif elem_type == "node_inst":
                    s += (str(x.inst_name))
                elif elem_type == "parameter":
                    s += (str(x.class_name)+"="+str(x.inst_name))
                elif elem_type == "function":
                    s += (str(x.class_name))
                else:
                    pass
                s += " "
            else:
                if elem_type == "instance":
                    self.w_instanciate(x)
                else:
                    pass
        if len(s) > 0:
            self.w_line(self.obj.cmd[cmd] + " " + s)

    def w_dict(self, dic, elem_type="node_inst", cmd="inline"):
        for bus, l in dic.items():
            self.w_list(l, elem_type=elem_type, cmd=cmd) 

    def w_base(self):
        self.w_line("* open file")
        if self.file_type == "top":
            self.w_line(".end")
            self.line_idx = self.line_idx-1
        elif self.file_type == "module":
            self.w_line(".subckt " + self.obj.module_name)
            self.w_line(".ends")
            self.line_idx = self.line_idx-1
        else:
            pass

    def w_stmnt(self):
        for key, val_list in self.obj.stmnt.items():
            for val in val_list:
                line = self.obj.cmd[key] + " " + val
                self.w_line(line)

    def w_instanciate(self, inst):
        self.w_line(inst.inst_name)
        self.w_dict(inst.node, elem_type="node_inst")
        if inst.module_type not in ["basic"]:
            self.w_line(self.obj.cmd["inline"] + " " + inst.module_name)
        self.w_dict(inst.param, elem_type="parameter")
        self.w_dict(inst.function, elem_type="function")
        self.w_line("")

    def w_module(self):
        self.w_dict(self.obj.node, elem_type="node_class")
        self.w_dict(self.obj.param, elem_type="parameter")
        self.w_line("")
        self.w_dict(self.obj.sub_inst, elem_type="instance")

    def w_top(self):
        return

    def w_data(self):
        return

    def w_global(self, alter_idx=-1):
        self.w_dict(self.obj.global_param, elem_type="parameter", cmd="parameter")
        self.w_dict(self.obj.global_node, elem_type="node_class", cmd="node")

    def write(self, alternate):
        if alternate > 0:
            if self.file_type != "data":
                raise ValueError("Alternate is not allowed except data type file.")
            else:
                for i in range(alternate):
                    self.w_base()
                    self.w_stmnt()
                    self.w_global(alter_idx=i)
        elif alternate == 0:
            raise ValueError("alternate should be equal or larger than 0.")
        else:
            self.w_stmnt()
            self.w_global()
            self.w_base()
            if self.file_type == "top":
                pass
            elif self.file_type == "module":
                self.w_module()
            elif self.file_type == "data":
                pass
            with open(self.file_path, "w") as file_handler:
                file_handler.writelines(self.line_handler)
