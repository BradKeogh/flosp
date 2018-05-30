import pandas as pd
import numpy as np
import warnings

from flosp import basic_tools
from flosp import _core
from flosp import _expected_file_structures
from flosp import _plotting

class data():
    """ class to store all data and meta """

    def __init__(self,name,save_path,valid_years):
        self.name = name
        self.save_path = _core.path_add_child_structure(save_path, self.name)
        self.valid_years = valid_years



class analyse():
    """ Class to manage hospital data importing.
    Input:
    name, str, name for class (will be used in filename saving.)
    save_path, str, e.g. './../../3_Data/' (must use parent folder).
    valid_years, list, a list of the years (ints) for which there are complete records.
    """
    #from flosp.ED import ED
    def __init__(self,name,save_path,valid_years):
        self.data = data(name,save_path,valid_years)
        self.ED = ED(self.data)
        self.IP = IP(self.data)
        self.load_processed_data()

    def set_valid_years(self, valid_years):
        """
        Give valid years of
        input: list, a list of the years (ints) for which there are complete records
        """
        self.data.valid_years = valid_years
        return

    def set_save_path(self,save_path):
        """sets path for saving any data files to. Use the parent folder, all data will be automatically placed within a 'procesed/name/' folder.'
        Input,str, e.g. './../../3_Data/'
        """
        self.data.save_path = _core.path_add_child_structure(save_path, self.data.name)
        return

    def load_processed_data(self):
        """
        finds and imports data that has been cleaned with .name attribute of the class you are calling from.
        """
        _core.message('attemping to import processed dataframes.')

        possible_pkls = _expected_file_structures.possible_pkls_list # get list of possible pkl files

        for i in possible_pkls:
            search_filename = self.data.name + i #add the class instance name to file structure.
            exists = _core.search_for_pkl(self.data.save_path,search_filename) # find if file exists

            if exists == True:
                full_path = self.data.save_path + search_filename
                attribute_name = 'data' + i[:-4]
                setattr(self.data, attribute_name , pd.read_pickle(full_path) ) #remove .pkl
        return

class ED():
    """
    doc here
    """
    def __init__(self,data):
        self._data = data
        self.plot = _plotting.plotED(data)

    def print_hi(self):
        print('Helllo!')
        print(self._data.name)
        return

    def filter():
        """ """
        return

    def auto_plot():
        """ calls and attempts all the known plots. Messages if there is an error creating any of them. """

        return

class IP():
    """doc here """
    def __init__(self,data):
        self._data = data
        pass
