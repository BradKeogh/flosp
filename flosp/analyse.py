
#from flosp import core

class analyse(object):
    """ Class to manage hospital data importing.
    Input: name, string, for all file prefixs.
    """
    def __init__(self,name):
        self.name = name

        ## make methods accesible with .
        #self.ioED = ioED(self.name)
        #setattr(self, 'ioED', ioED)

    def my_func(self):
        answer = core.core_func2()
        print(answer)
        return (answer)
