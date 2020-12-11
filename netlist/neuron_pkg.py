from core.spmodule import *

from netlist.basic import *
from netlist.xbar import *
from netlist.neuron import *

def design_neuron_pkg(self, npkg_args):
    is_univ = False
    n_tiles, n_rows, n_cols, n_outs = npkg_args
    # 0-a. INCLUDE: necesarry submodules
    self.include_stmnt("include:neuron")
    self.include_stmnt("include:cbar")
    # 0-b. INCLDUE: local parameters
    # 1-a. DEFINE: external nodes
    if is_univ==True:
        self.define_local("node:in", n_tiles, n_rows, n_cols)
    else:
        self.define_local("node:in", n_tiles, n_rows)
    self.define_local("node:out", n_outs)
    self.define_local("node:offset")
    self.define_local("node:sen")
    # 1-b. DEFINE: parameters
    self.define_local("parameter:pw", n_tiles, n_rows, n_cols)
#self.define_local("parameter:pvth", n_tiles, n_rows, n_cols) 
    # 2-a. ARRANGE:
    tile_module_name = "tile"
    tile_inst_name = tile_module_name + "_{}"
    tile_design, tile_design_args = design_cbar, (n_rows, n_cols)
    for t in range(n_tiles):
        _tile_inst_name = tile_inst_name.format(t)
        tile_inst = Module(module_name=tile_module_name,
                           inst_name=tile_inst_name,
                           design=design_cbar,
                           design_args=tile_design_args)
        self.instanciate(inst=tile_inst)
        for row in range(n_rows):
            for col in range(n_cols):
                if is_univ==True:
                    self.connect(m1=self, n1="in:in_{}_{}_{}".format(t, row, col),
                                 m2=tile_inst, n2="in:in_{}_{}".format(row, col))
                else:
                    self.connect(m1=self, n1="in:in_{}_{}".format(t, row),
                                 m2=tile_inst, n2="in:in_{}_{}".format(row, col))
                self.assign(m=tile_inst, 
                            p="tw:tw_{}_{}".format(row,col), 
                            p_assgn="pw:pw_{}_{}_{}".format(tile, row, col))


    neuron_module_name = "neuron"
    neuron_inst_name = neuron_module_name + "_{}"
    neuron_design, neuron_design_args = design_neuron, design_neuron_args
    for o in range(n_outs):
        _neuron_inst_name = neuron_inst_name.format(o)
        neuron_inst = Module(module_name=neuron_module_name,
                             inst_name=neuron_inst_name,
                             design=neuron_design,
                             design_args=neuron_design_args)
        self.instanciate(inst=neuron_inst)
        self.connect(m1=self, n1="offset:",
                     m2=neuron_inst, n2="offset:")
        self.connect(m1=self, n1="sen:",
                     m2=neuron_inst, n2="sen:")
        self.connect(m1=self, n1="out:out_{}".format(o),
                     m2=neuron_inst, n2="out:")
        for t in range(n_tiles):
            n_pairs = int(n_col /2)
            for p in range(n_pairs):
                col_pos = 2*l
                col_neg = col_pos+1
                self.connect(m1=self.sub_inst[tile_module_name][t], n1="ps:ps_{}".format(col_pos),
                             m2=neuron_inst, n2="pos:pos_{}".format(p))
                self.connect(m1=self.sub_inst[tile_module_name][t], n1="ps:ps_{}".format(col_neg),
                             m2=neuron_inst, n2="pos:pos_{}".format(p))

    # 3. DRAW
    self.print_stat()
    self.generate()

    return print("Neuron Pakage Design Complete!")

