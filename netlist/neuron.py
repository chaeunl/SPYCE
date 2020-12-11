from core.spmodule import *

from netlist.basic import *
from netlist.act import *

def design_neuron(self, neuron_args):
    n_inputs = neuron_args
    n_pairs = int(n_inputs/2)
    # 0-a. INCLUDE: necesarry submodules
    self.include_stmnt("include:partial_ckt")
    # 0-b. INCLDUE: local parameters
    # 1-a. DEFINE: external nodes
    self.define_local("node:pos", n_pairs)
    self.define_local("node:neg", n_pairs)
    self.define_local("node:out", 1)
    self.define_local("node:offset", 1)
    self.define_local("node:sen", 1)
    # 1-b. DEFINE: parameters
    # 2-a. ARRA:
    ps_module_name = "partial_ckt"
    ps_inst_name = ps_module_name + "_{}"
    for p in range(n_pairs):
        _ps_inst_name = ps_inst_name.format(p)
        ps_inst = Module(module_name=ps_module_name,
                         inst_name=_ps_inst_name,
                         design=None,
                         design_args=None)
        self.instanciate(inst=ps_inst)
        self.connect(m1=self, n1="pos:pos_{}".format(p),
                     m2=ps_inst, n2="pos:")
        self.connect(m1=self, n1="neg:neg_{}".format(p),
                     m2=ps_inst, n2="neg:")
        self.connect(m1=self, n1="offset:offset_0",
                     m2=ps_inst, n2="offset:")
        self.connect(m1=self, n1="sen:sen_0",
                     m2=ps_inst, n2="SEN:")

    act_module_name = "act{}".format(n_pairs)
    act_inst_name = act_module_name + "_{}"
    act_inst_name = act_inst_name.format(0)
    act_inst = Module(module_name=act_module_name,
                      inst_name=act_inst_name,
                      design=design_act,
                      design_args=1)
    self.include_stmnt("include:act{}".format(n_pairs))
    self.instanciate(act_inst)
    for p in range(n_pairs):
        self.connect(m1=self.sub_inst[ps_module_name][p], n1="out:out_0",
                     m2=act_inst, n2="in:in_{}".format(p),
                     node_name="pout_{}".format(p))
    # 3. DRAW
    self.print_stat()
    self.write(overwrite=True)

    return print("Neuron Design Complete!")
