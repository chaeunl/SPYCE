
import numpy as np

class Initializer():
    def __init__(self, 
                shape, 
                 init_type="uniform", 
                 quant_level=-1, 
                 mean=0.,
                 std=1.):
        self.shape = shape
        self.init_type, self.quant_level = init_type, quant_level
        self.mean, self.std, self.var = mean, std, std*std

    def run(self):
        if self.init_type=="uniform":
            ub, lb = self.mean + np.sqrt(3)*self.std, self.mean - np.sqrt(3)*self.std
            if self.quant_level < 0:
                data = np.random.uniform(low=lb, high=ub, size=self.shape)       
            else:
                scale, offset = 0.5*(ub - lb), 0.5* (ub + lb)
                data = np.random.randint(low=-self.quant_level, high=self.quant_level+1, size=self.shape)/quant_level
                data = scale * data + offset

        elif self.init_type=="gaussian":
            ub, lb = self.mean + 3*self.std, self.mean - 3*self.std
            data = np.random.normal(loc=self.mean, scale=self.std, size=self.shape)
            data[data > ub], data[data < lb] = ub, lb
            if self.quant_level < 0:
                pass
            else:
                quant_step = (ub - lb)/(self.quant_level-1)
                bins = np.arange(lb, ub + quant_step, quant_step) - (quant_step/2.)
                data_digitized = np.digitize(data, bins).reshape(-1)
                data = bins[data_digitized - 1] + (quant_step/2.)
        else:
            print("The {} is not defined".format(self.init_type))

        return data

