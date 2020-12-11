from collections import OrderedDict

from core.sp import SP
from core.initializer import *
from utils.global_functions import *

class SPData(SP):
    """
    Usage:
    dataset = SPData()
    dataset.generate(data_type="input:rram_vt", shape=(10000,2,32,8))
    dataset.generate(data_type="hidden:tr_length")
    """
    def __init__(self, 
                 file_dir="./", 
                 file_name="input_data", 
                 random_init=True, 
                 weight_init="uniform", 
                 activation_init="uniform", 
                 ref_map=None,
                 design=None,
                 design_args=None):
        super(SPData,self).__init__(file_dir=file_dir, 
                                    file_name=file_name,
                                    file_type="data",
                                    design=None,
                                    design_args=None)
        if random_init==True:
            if ref_map != None:
                raise ValueError("When random_init is True, ref_map should be None.")
            else:
                self.weight_init, self.activation_init = weight_init, activation_init
        else:
            self.ref_map = ref_map
        self.data_dict =  OrderedDict([])

        if design==None:
            if ref_map == None:
                raise ValueError("There must exist a ref map or design.")
        else:
            SPData.design = design
            if design_args==None:
                self.design()
            else:
                self.design(design_args)

    def read(self,
             data_type,
             ref_map):
        return

    def write(self, overwrite=False):
        super(SPData, self).write(overwrite=overwrite)

    def generate(self,
                 data_type,
                 shape,
                 init_type="uniform",
                 quant_level=-1,
                 mean=0.5,
                 std=1.):
        """
        data_type = str. "input/hidden/output:variable name". e.g., "input:rram_vt", "hidden:tr_length"
        shape = tuple. "(time_len, batch_size, input_dims #0, input_dims #1, ...)" 
        """
        data_map = Initializer(shape=shape, 
                               quant_level=-1,
                               mean=0.5,
                               std=1.).run()
        data_class, data_name = decipher(data_type)
        if not data_class in self.data_dict.keys():
            self.data_dict[data_class] = OrderedDict([])
        if not data_name in self.data_dict[data_class].keys():
            self.data_dict[data_class][data_name] = data_map
        else:
            raise ValueError("The data to generate, {}, is already called.".format(data_name))

    def print_stat(self):
        print("\n","="*20, "The information for Data file","="*20)
        for data_type, dic in self.data_dict.items():
            self._print_dict(data_type, dic)
