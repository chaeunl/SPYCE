
import numpy as np

class Initializer():
    def __init__(self, batch_size, input_dims, output_dims, init_type="uniform", quant_level=-1, interval=[-1,1]):
        self.batch_size, self.input_dims, self.output_dims = batch_size, input_dims, output_dims
        self.init_type, self.quant_bit = init_type, quant_bit
        self.ub, self.lb = self.interval

        self.data = self._run()

    def _run(self):
        if self.init_type="uniform":
            if self.quant_level < 0:
                data = np.random.uniform(low=self.lb, high=self.ub, size=(self.batch_size, self.input_dims, self.output_dims)       
            else:
                scale, offset = 0.5*(self.ub - self.lb), 0.5* (self.ub + self.lb)
                data = np.random.randint(low=-self.quant_level, high=self.quant_level+1, size=(self.batch_size, self.input_dims, self.output_dims))/quant_level
                data = scale * data + offset

        else:
            print("The {} is not defined".format(self.init_type))

        return data

