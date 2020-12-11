from core.sp import *

def design_env(self, env_args):
    temp = env_args
    self.include_stmnt("temperature:25")
    self.include_stmnt("include:interface")
    self.write()
