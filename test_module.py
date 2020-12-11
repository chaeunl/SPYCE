from netlist.basic import *
from netlist.xbar import *
from netlist.act import *
from netlist.neuron import *
from netlist.neuron_pkg import *
from netlist.data import *

from netlist.env import *

from core.spmodule import *
from core.spdata import *

if __name__=="__main__":
#    v = Module(module_name="v1",
#               inst_name="v1_0",
#               design=design_v,
#               design_args="DC 1v")
#    cbar = Module(module_name="cbar2x3",
#                  inst_name="cbar2x3_0",
#                  design=design_cbar,
#                 design_args=(2,3))
#    act = Module(module_name="act2",
#                 inst_name="act2_0",
#                 design=design_act,
#                 design_args=(2))
    neuron = Module(module_name="neuron2",
                    inst_name="neuron2_0",
                    design=design_neuron,
                    design_args=(2))
#    dataset = SPData(design=design_data,
#                     design_args=(1,2,3,4))
#    env = SP(file_name="env",
#             design=design_env,
#             design_args=(25),
#             )
