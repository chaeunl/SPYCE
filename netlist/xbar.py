from core.spmodule import *
from netlist.basic import *

def design_cbar(self, cbar_args):
    is_univ = False
    n_rows, n_cols = cbar_args
    # 0-a. INCLUDE: necessary submoduels
    self.include_stmnt("include:1t1r")
    # 0-b. INCLUDE: local parameters
    self.define_global("parameter:rsTE", val=20)
    self.define_global("parameter:rsBE", val=200)
    self.define_global("parameter:rsLD", val=0)
    self.define_global("parameter:rsLK", val=0)

    # 1-a. DEFINE: external nodes
    if is_univ==True:
        self.define_local("node:in", n_rows, n_cols)
    else:
        self.define_local("node:in", n_rows)
    self.define_local("node:ps", n_cols)
    # 1-b. DEFINE: parameters
    self.define_local("parameter:tw", n_rows, n_cols)

    # 2-a. ARRANGE: load resistors btw/ word decoder
    rld_module_name = "rld"
    rld_inst_name = rld_module_name + "_{}"
    for row in range(n_rows):
        if is_univ==True:
            __rld_inst_name = _rld_inst_name + "_{}"
            for col in range(n_cols):
                __rld_inst_name = __rld_inst_name.format(row,col)
                rld_inst = Module(module_name = rld_module_name, 
                                  inst_name = __rld_inst_name,
                                  design = design_r,
                                  design_args = None)
                self.instanciate(inst=rld_inst)
                self.assign(m=rld_inst, p="R:", p_assgn="rsLD:")
                self.connect(m1=self, n1="in:in_{}_{}".format(row,col),
                             m2=rld_inst, n2="n:n_0")
        else:
            _rld_inst_name = rld_inst_name.format(row)
            rld_inst = Module(module_name = rld_module_name,
                              inst_name = _rld_inst_name,
                              design = design_r,
                              design_args = None)
            self.instanciate(inst=rld_inst)
            self.assign(m=rld_inst, p="R:", p_assgn="rsLD:")
            self.connect(m1=self, n1="in:in_{}".format(row),
                         m2=rld_inst, n2="n:n_0")
    # 2-b. ARRANGE: top layer resistors
    if is_univ!=True:
        rt_module_name = "rt"
        rt_inst_name = rt_module_name + "_{}_{}"
        for row in range(n_rows):
            for col in range(n_cols-1):
                __rt_inst_name = rt_inst_name.format(row,col)
                rt_inst = Module(module_name = rt_module_name,
                                 inst_name = __rt_inst_name,
                                 design = design_r,
                                 design_args = None)
                self.instanciate(inst = rt_inst)
                self.assign(m=rt_inst, p="R:", p_assgn="rsTE:")
                if col < 1:
                    m1_inst = self.sub_inst[rld_module_name][row]
                else:
                    m1_idx = row*(n_cols-1) + (col-1)
                    m1_inst = self.sub_inst[rt_module_name][m1_idx]
                self.connect(m1=m1_inst, n1="n:n_1",
                             m2=rt_inst, n2="n:n_0",
                             node_name="u_{}_{}".format(row, col))
    # 2-c. ARRANGE: parasite resistros to output nodes
    rlk_module_name = "rlk"
    rlk_inst_name = rlk_module_name + "_{}"
    for col in range(n_cols):
        _rlk_inst_name = rlk_inst_name.format(col)
        rlk_inst = Module(module_name = rlk_module_name,
                          inst_name = _rlk_inst_name,
                          design = design_r,
                          design_args = None)
        self.instanciate(inst=rlk_inst)
        self.assign(m=rlk_inst, p="R:", p_assgn="rsLK:")
        self.connect(m1=self, n1="ps:ps_{}".format(col),
                     m2=rlk_inst, n2="n:n_0")
    # 2-d. ARRANGE: bottom layer resistors
    if is_univ!=True:
        rb_module_name = "rb"
        rb_inst_name = rb_module_name + "_{}_{}"
        for row in range(n_rows-1):
            for col in range(n_cols):
                __rb_inst_name = rb_inst_name.format(row,col)
                rb_inst = Module(module_name = rb_module_name,
                                 inst_name = __rb_inst_name,
                                 design = design_r,
                                 design_args = None)
                self.instanciate(inst=rb_inst)
                self.assign(m=rb_inst, p="R:", p_assgn="rsBE:")
                if row < 1:
                    m1_inst = self.sub_inst[rlk_module_name][col]
                else:
                    m1_idx = (row-1)*(n_cols) + col
                    m1_inst = self.sub_inst[rb_module_name][m1_idx]
                self.connect(m1=m1_inst, n1="n:n_1",
                             m2=rb_inst, n2="n:n_0",
                             node_name="b_{}_{}".format(row,col))
    # 2-e. ARRANGE: cells connect between top and bottom layer
    rram_module_name = "1t1r"
    rram_inst_name = rram_module_name + "_{}_{}"
    node_name_t, node_name_b = None, None
    for row in range(n_rows):
        for col in range(n_cols):
            __rram_inst_name = rram_inst_name.format(row, col)
            rram_inst = Module(module_name = rram_module_name,
                               inst_name = __rram_inst_name,
                               design = None,
                               design_args = None)
            self.instanciate(inst=rram_inst)
            self.assign(m=rram_inst, p="conductance:", p_assgn="tw:tw_{}_{}".format(row,col))
            if col < 1:
                mrt_inst = self.sub_inst[rld_module_name][row]
            else:
                mrt_idx = row*(n_cols-1) + (col-1)
                mrt_inst = self.sub_inst[rt_module_name][mrt_idx]
                if col == (n_cols-1):
                    node_name_t = "u_{}_{}".format(row,col)
            if row < 1:
                mrb_inst = self.sub_inst[rlk_module_name][col]
            else:
                mrb_idx = (row-1)*(n_cols) + col 
                mrb_inst = self.sub_inst[rb_module_name][mrb_idx]
                if row == (n_rows-1):
                    node_name_b = "b_{}_{}".format(row,col)
            self.connect(m1=mrt_inst, n1="n:n_1",
                         m2=rram_inst, n2="row:",
                         node_name=node_name_t)
            self.connect(m1=rram_inst, n1="col:",
                         m2=mrb_inst, n2="n:n_1",
                         node_name=node_name_b)
            node_name_t, node_name_b = None, None
    self.print_stat()
    # 3. DRAW:
    self.write()
    return print("Crossbar Design complete!")

