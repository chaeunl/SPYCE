from core.sp import *
from core.spmodule import *

class BasicModule(Module):
    def __init__(self,
                 module_name,
                 inst_name,
                 design=None,
                 design_args=None):
        super(BasicModule, self).__init__(module_name=module_name,
                                          inst_name=inst_name,
                                          file_dir=None,
                                          design=design,
                                          design_args=design_args)
        self.function = OrderedDict()
