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
    def __init__(self,name,save_path):
        self.name = name
        self.set_save_path(save_path)

    def set_save_path(self,save_path):
        """sets path for saving any data files to. Use the parent folder, all data will be automatically placed within a 'procesed/classname/' folder.'
        Input,str, e.g. './../../3_Data/'
        """
        save_path = _core.path_backslash_check(save_path) #ensure that path has / at end
        self.save_path = save_path + 'processed/' + self.name + '/' #make save_path an attribute
        return

    def my_func(self):
        answer = core.core_func2()
        print(answer)
        return (answer)

    def load_processed_data(self):
        """
        finds and imports data that has been cleaned with .name attribute of the class you are calling from.
        """
        _core.message('attemping to import processed dataframes.')

        possible_pkls = _expected_file_structures.possible_pkls_list # get list of possible pkl files

        for i in possible_pkls:
            search_filename = self.name + i #add the class instance name to file structure.
            exists = _core.search_for_pkl(self.save_path,search_filename) # find if file exists

            if exists == True:
                full_path = self.save_path + search_filename
                attribute_name = '_data' + i[:-4]
                setattr(self, attribute_name , pd.read_pickle(full_path) ) #remove .pkl
        return
