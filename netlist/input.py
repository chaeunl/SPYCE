
def design_input(input_args):
    n_inputs = input_args
    self.define_global("parameter:initial_dealy", "2ns")
    self.define_global("parameter:tr")
    self.define_global("parameter:tf")
    self.define_global("parameter:width")
    self.define_global("parameter:period")

    self.define_local("node:in", 1)
    self.define_local("parameter:pact", 1)

    v_inst = Module(module_name = ?,
                    inst_name = ?,
                    design = design_v,
                    design_args = "function:pulse(0V 'pact' 'initial_delay' 'tr' 'tf' 'width' 'period')") 
    self.instantiate(inst=v_inst)
    self.connect(m1=self, n1=,
                 m2=, n2=)


