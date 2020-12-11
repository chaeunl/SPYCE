
from netlist.basic import design_v

def design_interface(self):
    self.include_stmnt("include:neuron_pkg")    # include neuron_pkg files
    self.include_stmnt("include:input_pkg")    # include input_pkg files
    self.include_stmnt("include:inst")    # include inst file
    self.include_stmnt("include:opt")    # include opt file
    self.include_stmnt("include:measure")    # include measure file
    self.include_stmnt("include:input_data")    # include data file

    self.define_local("parameter:dd_initial_voltage", "0V")
    self.define_local("parameter:dd_last_volate", "0V")
    self.define_local("parameter:dd_delay", "1.95ns")
    self.define_local("parameter:dd_tr", "30ps")
    self.define_local("parameter:dd_tf", "30ps")
    self.define_local("parameter:dd_width", "1.05ns")
    self.define_local("parameter:dd_period", "10ns")

    self.define_local("parameter:sen_initial_voltage", "0V")
    self.define_local("parameter:sen_last_voltage", "0.8V")
    self.define_local("parameter:sen_delay")
    self.define_local("parameter:sen_tr")
    self.define_local("parameter:sen_tf")
    self.define_local("parameter:sen_width")
    self.define_local("parameter:sen_period")

    self.define_local("parameter:offset_initial_voltage")
    self.define_local("parameter:offset_last_voltage")
    self.define_local("parameter:offset_delay")
    self.define_local("parameter:offset_tr")
    self.define_local("parameter:offset_tf")
    self.define_local("parameter:offset_width")
    self.define_local("parameter:offset_period")

    self.define_global("node:vdd")
    self.define_global("node:vss")

    vdd_inst = Module(module_name="vdd",
                      inst_name="vdd",
                      design=design_v,
                      design_args=("pulse",
                                   "dd_initial_voltage",
                                   "dd_last_voltage",
                                   "dd_delay",
                                   "dd_tr",
                                   "dd_tf",
                                   "dd_width",
                                   "dd_period"))
    vsen_inst = Module(module_name="vsen",
                       inst_name="vsen",
                       design=design_v,
                       design_args=("pulse",
                                    "sen_initial_voltage",
                                    "sen_last_voltage",
                                    "sen_delay",
                                    "sen_tr",
                                    "sen_tf",
                                    "sen_width",
                                    "sen_period"))
    voffset_inst = Module(module_name="voffset",
                          inst_name="voffset",
                          design=design_v,
                          design_args=("pulse",
                                       "offset_initial_voltage",
                                       "offset_last_voltage",
                                       "offset_delay",
                                       "offset_tr",
                                       "offset_tf",
                                       "offset_width",
                                       "offset_period"))
    vss_inst = Module(module_name="vss",
                      inst_name="vss",
                      design=design_v,
                      design_args=("none",
                                   "0"))
    # 3. DRAW:
    self.write()
    return print("Interface Design complete!")
