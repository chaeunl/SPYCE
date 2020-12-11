def design_r(self):
    # 0. INCLUDE:
    # 1. DEFINE:
    self.define_local("node:n", 2)
    self.define_local("parameter:R")
    # 2. ARRANGE:
    # 3. DRAW:
    self.print_stat()
    return

def design_v(self, v_args):
    self.define_local("node:n", 2)
    self.define_local("function:"+v_args)
    self.print_stat()
    self.write()
    return
