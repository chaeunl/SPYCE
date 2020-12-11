import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nsyn", type=int,
                    default = 16, 
                    help="Specify the number of input synapses")
parser.add_argument("--Xbar", type=int,
                    default = 4,
                    help="Specifiy the row size of Xbar; default is 32x32 Xbar")
parser.add_argument("--weight_init", type=str,
                    default="uniform",
                    help="Specify the distribution from which weigths are sampled; Gaussian(gaussian) or Uniform(uniform)")
parser.add_argument("--input_init", type=str,
                    default="uniform",
                    help="Specify the distribution from which inputs are sampled; Gaussian(gaussian) or Uniform(uniform)")
parser.add_argument("--pkg", type=int,
                    default=2,
                    help="Specify the number of neuons in a package.")
parser.add_argument("--precision", type=int,
                    default=4,
                    help="Specify the number of significant bits.")
parser.add_argument("--monte", type=int,
                    default=2,
                    help="Specify the number of monte carlo simulations.")
parser.add_argument("--pinpoints", type=int,
                    default=1,
                    help="Specify the number of points in the time window.")

parser.add_argument("--batch_size", type=int,
                    default=1,
                    help="Specify the size of mini batch")
parser.add_argument("--root", type=str,
                    default="./run/",
                    help="Specify the root path of this file.")
parser.add_argument("--data", type=str,
                    default="./data/",
                    help="Specify the path to save the result.")
parser.add_argument("--file_idx", type=int,
                    default=0,
                    help="Specify the index number of each file." )
parser.add_argument("--ref_map", type=str,
                    default=None,
                    help="Specify the path of maps for weights and activations.")


is_univ=True    # determine wheter each cell in xbar is applied w/ different input voltage or not.

def design_r(self):
    # 0. INCLUDE:
    # 1. DEFINE:
    self.define_what("node:n", 2)
    self.define_what("parameter:R")
    # 2. ARRANGE:
    # 3. DRAW:
    return

def design_cbar(self, cbar_args):
    n_row, n_col = cbar_args
    # 0-a. INCLUDE: necessary submoduels
    self.include_stmnt("incldue","1t1r")
    # 0-b. INCLUDE: local parameters
    self.include_stmnt("parameter","rsTE",20)
    self.include_stmnt("parameter","rsBE",200)
    self.include_stmnt("parameter","rsLD",0)
    self.include_stmnt("parameter","rsLK",0)

    # 1-a. DEFINE: external nodes
    if is_univ==True:
        self.define_what("node:in", n_rows, n_cols)
    else:
        self.define_what("node:in", n_rows)
    self.define_what("node:ps", n_cols)
    # 1-b. DEFINE: parameters
    self.define_what("paramter:tw", n_rows, n_cols)

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
                self.connect(m1=self, n1="in:in_{}_{}".format(row,col),
                             m2=rld_inst, n2="n:n_0")
        else:
            _rld_inst_name = rld_name.format(row)
            rld_inst = Module(module_name = rld_module_name,
                              inst_name = _rld_inst_name,
                              design = design_r,
                              design_args = None)
            self.instanciate(inst=rld_inst)
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
                if col < 1:
                    m1_inst = self.sub_inst[rld_module_name][row]
                else:
                    m1_idx = row*(n_cols-1) + col
                    m1_inst = self.sub_inst[rt_module_name][m1_idx]
                self.connect(m1=m1_inst, n1="n:n_1",
                             m2=rt_inst, n2="n:n_0",
                             node_name="u_{}_{}".format(row, col))
    # 2-c. ARRANGE: cells connect between top and bottom layer
    rram_module_name = "rram"
    rram_inst_name = rram_module_name + "_{}_{}"
    for row in range(n_rows):
        for col in range(n_cols):
            __rram_inst_name = rram_inst_name.format(row, col)
            rram_inst = Module(module_name = rram_module_name,
                               inst_name = __rram_inst_name,
                               design = None,
                               design_args = None)
            self.instanciate(inst=rram_inst)
            self.connect(m1=, n1=,
                         m2=, n2=)
    # 2-d. ARRANGE: bottom layer resistors
    if is_univ!=True:
        rb_module_name = "rb"
        rb_inst_name = rb_module_name + "_{}_{}"
        for row in range(n_rows):
            for col in range(n_cols-1):
                __rb_inst_name = rb_inst_name.format(row,col)
                rb_inst = Module(module_name = rb_module_name,
                                 inst_name = __rb_inst_name,
                                 design = design_r,
                                 design_args = None)
                self.instanciate(inst=rb_inst)
                self.connect(,rt)

    # 2-e. ARRANGE: parasite resistros to output nodes
    for col in range(n_cols):
        _rlk_name = rlk_name.format(col)
        rlk_inst = Module(module_name = "r",
                          inst_name = _rlk_name,
                          design = design_r,
                          design_args = None)
        self.instanciate(inst=rlk_inst)
        self.connect(m1=, n1=,
                     m2=, n2=)

    # 3. DRAW:
    self.geneterate()
    return print("Crossbar Design complete!")

    
def design_input():
    # 0-a. INCLUDE: necessary submoduels
    cbar.include_file()
    # 0-b. INCLUDE: local parameters
    cbar.include_param()

    # 1-a. DEFINE: external nodes
    inputo.define_node("output")
    # 1-b. DEFINE: parameters
    # 2. ARRANGE: pulse-type voltage source
    vi = v.instanciate()
    # 3. DRAW:
    inputo.generate()
    return

def design_input_pkg(n_syn, n_neuron, input_pkg):
    # 0-a. INCLUDE: necessary submoduels
    input_pkg.include_file()
    # 0-b. INCLUDE: local parameters
    input_pkg.include_param()
    
    # 1-a. DEFINE: external nodes
    input_pkg.define_node("input")
    input_pkg.define_node("output")
    # 1-b. DEFINE: parameters

    # 2-a. ARRANGE: 
    for i in range(n_syn):
        for j in range(n_neuron):
            inputo.instanciate()
            input_pkg.connect(,inputo)
    # 3. DRAW:
    input_pkg.generate()
    return print("Input package Design complete!")

def design_neuron_pkg(n_syn, n_neuron, cbar, neuron_pkg, neuron):
    # 0-a. INCLUDE: necessary submoduels
    neuron_pkg.include_file()
    # 0-b. INCLUDE: local parameters
    neuron_pkg.include_param()

    # 1-a. DEFINE: external nodes
    neuron_pkg.define_node("input")
    neuron_pkg.define_node("control")
    neuron_pkg.define_node("output")
    # 1-b. DEFINE: parameters
    neuron_pkg.define_param()

    # 2. ARRANGE: crossbars
    c1 = cbar.instanciate()
    c2 = cbar.instanciate()
    n1 = neuron.instanciate()

    neuron_pkg.connect(c1, n1)
    neuron_pkg.connect(c2, n1)

    # 3. DRAW:
    neuron_pkg.generate()
    return print("Neuron package Design complete!")

def design_interface():
    return

def design_env():
    return

if __name__=="__main__":
    r1 = Module(module_name="r", design=design_r, design_args)
    cbar64x2 = design_cbar(cbar, rram_cell)
