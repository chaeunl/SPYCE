from core.spmodule import *
from netlist.basic import *

def design_act(self, act_args):
    n_inputs = act_args
    # 0-a. INCLUDE: necesarry submodules
    self.include_stmnt("include:comp")
    # 0-b. INCLDUE: local parameters
    # 1-a. DEFINE: external nodes
    self.define_local("node:in", n_inputs)
    self.define_local("node:out")
    # 1-b. DEFINE: parameters
    # 2-a. ARRANGE:
    rlink_module_name = "rlink"
    rlink_inst_name = rlink_module_name + "_{}".format(n_inputs)
    for i in range(n_inputs):
        _rlink_inst_name = rlink_inst_name.format(i)
        rlink_inst = Module(module_name=rlink_module_name,
                            inst_name=_rlink_inst_name,
                            design=design_r,
                            design_args=None)
        self.instanciate(rlink_inst)
        self.connect(m1=self, n1="in:in_{}".format(i),
                     m2=rlink_inst, n2="n:n_0")
    comp_module_name = "comp"
    comp_inst_name = "comp_{}"
    _comp_inst_name = comp_inst_name.format(0)
    comp_inst = Module(module_name=comp_module_name,
                       inst_name=_comp_inst_name,
                       design=None,
                       design_args=None)
    self.instanciate(comp_inst)

    self.connect(m1=self, n1="out:",
                 m2=comp_inst, n2="out:")
    for i in range(n_inputs):
        self.connect(m1=self.sub_inst[rlink_module_name][i], n1="n:n_1",
                     m2=comp_inst, n2="p:",
                     node_name="pos_sum")

    ref_module_name = "vref"
    ref_inst_name = ref_module_name + "_{}"
    _ref_inst_name = ref_inst_name.format(0)
    ref_inst = Module(module_name=ref_module_name,
                      inst_name=_ref_inst_name,
                      design=design_v,
                      design_args="1.025V")
    self.instanciate(ref_inst)
    self.connect(m1=comp_inst, n1="n:",
                 m2=ref_inst, n2="n:n_0",
                 node_name="ref") 
    # 3. DRAW
    self.print_stat()
    self.write(overwrite=True)

    return 
