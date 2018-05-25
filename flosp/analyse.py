import pandas as pd
import numpy as np
import warnings

from flosp import basic_tools
from flosp import _core
from flosp import _expected_file_structures

class analyse:
    """ Class to manage hospital data importing.
    Input:
    name: str, name for class (will be used in filename saving.)
    """
    def __init__(self,name):
        self.name = name

    def my_func(self):
        answer = core.core_func2()
        print(answer)
        return (answer)

    def import_processed_data(self):
        """
        finds and imports data that has been cleaned with .name attribute of the class you are calling from.
        """
        _core.message('attemping to import processed dataframes.')

        return
