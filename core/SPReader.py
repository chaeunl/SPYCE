
class SPReader():
    def __init__(self, file_path):
        self.browse_custom_module(file_path) 

    def browse_custom_module(self, file_path):
        f = open(file_path, "r")
        for line in f.readlines():
            print(line)
            if line.find(".subckt") > -1:
                word_list = line.strip("\n").split(" ")
                print(word_list)
                for idx, word in enumerate(word_list):
                    if word == ".subckt":
                        self.module_name = word_list[idx+1]
       
            elif line.find("+") > -1:
                word_list = line.lstrip("+").strip(" ").split(" ")
                n_list, p_list = [], []
                for word in word_list:
                    if word.find("=") > -1:
                        _name = word.split("=")[0]
                        self.define_local("parameter:"+_name)
                    else:
                        _name = word
                        self.define_local("node:"+_name)


