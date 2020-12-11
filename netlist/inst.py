from core.spmodule import Module
from netlist.neuron_pkg import design_neuron_pkg
from netlist.input_pkg import design_input_pkg

def design_inst(self, inst_args):
    n_inputs, n_outputs = inst_args
    neuron_args = ()

    neuron_pkg_module_name = "neuron{}x{}".format(n_inputs, n_outputs)
    neuron_pkg_inst_name = neuron_pkg_module_name + "_inst"
    neuron_pkg = Module(module_name = neuron_pkg_module_name,
                        inst_name = neuron_pkg_inst_name,
                        design = design_neuron,
                        design_args = neuron_pkg_args)
    self.instanciate(neuron_pkg)

    input_pkg_module_name = "input{}".format(n_inputs)
    input_pkg_inst_name = input_pkg_module_anme + "_inst"
    input_pkg = Module(module_name = input_pkg_module_name,
                       inst_name = input_pkg_inst_name,
                       design = ,
                       design_args = input_pkg_args)
    self.instanciate(input_pkg)
