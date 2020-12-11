from core.spdata import *

def design_data(self, design_args):
    n_data, n_tiles, n_rows, n_cols = design_args
#    self.include_stmnt("incldue:lib")
    input_shape = (n_data, n_tiles, n_rows, n_cols)
    self.generate(data_type="input:conductance", shape=input_shape)
    self.generate(data_type="input:voltage", shape=input_shape)
    self.generate(data_type="input:vth", shape=input_shape)

    self.define_global("parameter:w", n_tiles, n_rows, n_cols, val=self.data_dict["input"]["conductance"][0])
    self.define_global("parameter:a", n_tiles, n_rows, n_cols, val=self.data_dict["input"]["voltage"][0])
    self.define_global("parameter:vt", n_tiles, n_rows, n_cols, val=self.data_dict["input"]["vth"][0])

#    for t in range(n_tiles):
#        for row in range(n_rows):
#            for col in range(n_cols):
#                self.assign("w:w_{}_{}_{}".format(t, row, col), val=self.data_dict["input"]["conductance"][t][row][col])
#                self.assign("a:a_{}_{}_{}".format(t, row, col), val=self.data_dict["input"]["voltage"][t][row][col])
#                self.assign("vt:vt_{}_{}_{}".format(t, row, col), val=self.data_dict["input"]["vth"][t][row][col])
#
    self.write(overwrite=True)
