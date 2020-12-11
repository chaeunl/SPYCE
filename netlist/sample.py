import core.spmodule import Module

def design_sample(self, sample_args):
    n_nodes, n_params = sample_args
    self.define_local("node:n", n_nodes)
    self.define_local("parameter:p", n_params)

    self.print_stat()
    self.write()
