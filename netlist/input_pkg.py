from core.spmodule import *

def design_input_pkg(self, ipkg_args):
    if is_univ == True:
        n_rows, n_cols = ipkg_args
    else:
        n_rows = ipkg_args
    # 0-a. INCLUDE: necesarry submodules
    self.include_stmnt("include:input")
    # 0-b. INCLDUE: local parameters
    # 1-a. DEFINE: external nodes
    if is_univ==True:
        self.define_local("node:in", n_rows, n_cols)
    else:
        self.define_local("node:in", n_rows)
    # 1-b. DEFINE: parameters
    if is_univ==True:
        self.define_local("parameter:pact", n_rows, n_cols)
    else:
        self.define_local("parameter:pact", n_rows)
    # 2-a. ARRANGE:
    input_module_name = "input"
    if is_univ==True:
        input_inst_name = "input_{}_{}"
        for row in range(n_rows):
            for col in range(n_cols):
                _input_inst_name = input_inst_name.format(row, col)
                input_inst = Module(module_name=input_module_name,
                                    inst_name=input_inst_name,
                                    design=None,
                                    design_args=None)
                self.instanciate(input_inst)
                self.connect(m1=self, n1="in:in_{}_{}".format(row, col),
                             m2=input_inst, n2="in:")
                self.assign(m=input_inst, p="pact:", p_assgn="pact_{}_{}".format(row, col))
    else:
        input_inst_name = "input_{}"
        for row in range(n_rows):
            _input_inst_name = input_isnt_name.format(row)
            input_inst = Module(module_name=input_module_name,
                                inst_name=input_inst_name,
                                design=None,
                                design_args=None)
            self.instanciate(input_inst)
            self.connect(m1=self, n1="in:in_{}".format(row, col),
                         m2=input_inst, n2="in:")
            self.assign(m=input_inst, p="pact:", p_assgn="pact_{}".format(row))
    # 3. DRAW
    self.print_stat()
    self.generate()
