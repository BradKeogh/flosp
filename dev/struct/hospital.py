import pandas as pd
import numpy as np

import core
import core2

class hosp(object):
    """ Class to manage hospital data importing.
    Input: name, string, for all file prefixs.
    """
    from core import core_func2
    def __init__(self,name):
        self.name = name
        
        ## make methods accesible with .
        #self.ioED = ioED(self.name)
        #setattr(self, 'ioED', ioED)
        
    def my_func(self):
        answer = core.core_func2()
        print(answer)
        return (answer)

class ioED(object):
    """
    ioED makes it easy to import ED data
    """
    def __init__(self,name):
        #hosp.__init__(self,name)
        core.core_func1()
        pass
    def load_csv(self):
        pass
    def clean(self):
        pass